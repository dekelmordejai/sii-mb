import csv
import hashlib
import io
import json
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.calculation import (
    ENGINE_VERSION,
    MethodConfig,
    RunInput,
    calculate,
    iso_date,
    number,
)
from app.connectors import CONNECTORS
from app.db import get_db
from app.models import Indicator, Method, Run, Source, User
from app.security import (
    audit,
    current_user,
    editor,
    grant_created,
    require_scope,
)

router = APIRouter(prefix="/api/v1", tags=["analysis"])


class SourceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=3, max_length=160)
    content: str = Field(min_length=1, max_length=1_000_000)
    types: dict[str, Literal["text", "number", "date"]] = Field(default_factory=dict, max_length=50)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Nombre demasiado corto")
        return value.strip()


def fetch(session, model, identifier):
    record = session.get(model, identifier)
    if record is None:
        raise HTTPException(404, "Registro no encontrado")
    return record


def source_view(item):
    return {
        "id": item.id,
        "name": item.name,
        "kind": item.kind,
        "sha256": item.sha256,
        "created_at": item.created_at,
        **json.loads(item.profile_json),
    }


def method_view(item):
    return {
        "id": item.id,
        "indicator_id": item.indicator_id,
        "version": item.version,
        "created_at": item.created_at,
        "config": json.loads(item.config_json),
        "status": "draft",
    }


def run_view(item):
    return {
        "id": item.id,
        "method_id": item.method_id,
        "source_id": item.source_id,
        "created_at": item.created_at,
        "engine_version": item.engine_version,
        "request": json.loads(item.request_json),
        "result": json.loads(item.result_json),
    }


@router.get("/sources")
def sources(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    scope = json.loads(user.scopes_json).get("sources", [])
    where = [] if user.role == "admin" or "*" in scope else [Source.id.in_(scope)]
    return {
        "items": [
            source_view(s)
            for s in session.scalars(
                select(Source)
                .where(*where)
                .order_by(Source.created_at.desc(), Source.id)
                .limit(limit)
                .offset(offset)
            )
        ],
        "total": session.scalar(select(func.count()).select_from(Source).where(*where)),
    }


@router.post("/sources", status_code=201)
def upload(
    payload: SourceInput,
    session: Session = Depends(get_db),
    user: User = Depends(editor),
):
    try:
        rows, profile = CONNECTORS["csv"].load(payload.content)
        columns = {c["name"] for c in profile["columns"]}
        if set(payload.types) - columns:
            raise ValueError("El esquema declara columnas inexistentes")
        for col in profile["columns"]:
            if col["name"] in payload.types:
                col["type"] = payload.types[col["name"]]
                for row in rows:
                    value = row[col["name"]]
                    if value and col["type"] == "number":
                        number(value)
                    if value and col["type"] == "date":
                        iso_date(value)
        profile["supervision"] = {
            "responsible_user_id": user.id,
            "change_detection": "immutable_snapshot_sha256",
            "fallback": "manual_new_csv_snapshot",
        }
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    item = Source(
        id=str(uuid4()),
        name=payload.name,
        kind="csv",
        content=payload.content,
        sha256=hashlib.sha256(payload.content.encode("utf-8")).hexdigest(),
        profile_json=json.dumps(profile),
    )
    session.add(item)
    grant_created(session, user, "sources", item.id)
    audit(
        session,
        user,
        "source.create",
        item.id,
        {"sha256": item.sha256, "rows": profile["row_count"]},
    )
    session.commit()
    return source_view(item)


@router.post("/sources/inspect")
def inspect_source(payload: SourceInput, user: User = Depends(editor)):
    try:
        _, profile = CONNECTORS["csv"].load(payload.content)
        return profile
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get("/sources/{source_id}")
def source(
    source_id: str,
    session: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    require_scope(user, "sources", source_id)
    return source_view(fetch(session, Source, source_id))


@router.post("/indicators/{indicator_id}/methods", status_code=201)
def add_method(
    indicator_id: str,
    payload: MethodConfig,
    session: Session = Depends(get_db),
    user: User = Depends(editor),
):
    require_scope(user, "indicators", indicator_id)
    indicator = fetch(session, Indicator, indicator_id)
    if not indicator.active:
        raise HTTPException(409, "Indicador desactivado")
    version = (
        session.scalar(select(func.max(Method.version)).where(Method.indicator_id == indicator_id))
        or 0
    ) + 1
    item = Method(
        id=str(uuid4()),
        indicator_id=indicator_id,
        version=version,
        config_json=payload.model_dump_json(),
    )
    session.add(item)
    audit(
        session,
        user,
        "method.create",
        item.id,
        {
            "indicator_id": indicator_id,
            "version": version,
            "config": payload.model_dump(mode="json"),
        },
    )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Se creó otra versión simultáneamente; reintenta") from None
    return method_view(item)


@router.get("/indicators/{indicator_id}/methods")
def methods(
    indicator_id: str,
    session: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    require_scope(user, "indicators", indicator_id)
    fetch(session, Indicator, indicator_id)
    return [
        method_view(m)
        for m in session.scalars(
            select(Method)
            .where(Method.indicator_id == indicator_id)
            .order_by(Method.version.desc())
        )
    ]


@router.post("/runs", status_code=201)
def execute(payload: RunInput, session: Session = Depends(get_db), user: User = Depends(editor)):
    method = fetch(session, Method, payload.method_id)
    require_scope(user, "indicators", method.indicator_id)
    require_scope(user, "sources", payload.source_id)
    if not fetch(session, Indicator, method.indicator_id).active:
        raise HTTPException(409, "Indicador desactivado")
    source = fetch(session, Source, payload.source_id)
    try:
        result = calculate(
            source.content,
            MethodConfig.model_validate_json(method.config_json),
            payload,
        )
    except ValueError as exc:
        audit(
            session,
            user,
            "run.failed",
            method.id,
            {"request": payload.model_dump(mode="json"), "error": str(exc)},
        )
        session.commit()
        raise HTTPException(422, str(exc)) from exc
    result["source_sha256"] = source.sha256
    item = Run(
        id=str(uuid4()),
        method_id=method.id,
        source_id=source.id,
        request_json=payload.model_dump_json(),
        result_json=json.dumps(result),
        engine_version=ENGINE_VERSION,
    )
    session.add(item)
    audit(
        session,
        user,
        "run.create",
        item.id,
        {"method_id": method.id, "source_id": source.id},
    )
    session.commit()
    return run_view(item)


@router.get("/runs")
def runs(
    indicator_id: str | None = None,
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    query = select(Run).join(Method)
    scopes = json.loads(user.scopes_json)
    if user.role != "admin":
        if "*" not in scopes.get("indicators", []):
            query = query.where(Method.indicator_id.in_(scopes.get("indicators", [])))
        if "*" not in scopes.get("sources", []):
            query = query.where(Run.source_id.in_(scopes.get("sources", [])))
    if indicator_id:
        query = query.where(Method.indicator_id == indicator_id)
    count = session.scalar(select(func.count()).select_from(query.subquery()))
    return {
        "items": [
            run_view(r)
            for r in session.scalars(
                query.order_by(Run.created_at.desc(), Run.id).limit(limit).offset(offset)
            )
        ],
        "total": count,
    }


@router.get("/runs/{run_id}")
def run(run_id: str, session: Session = Depends(get_db), user: User = Depends(current_user)):
    item = fetch(session, Run, run_id)
    require_scope(user, "sources", item.source_id)
    require_scope(user, "indicators", fetch(session, Method, item.method_id).indicator_id)
    return run_view(item)


@router.get("/runs/{run_id}/export")
def export(run_id: str, session: Session = Depends(get_db), user: User = Depends(current_user)):
    item = fetch(session, Run, run_id)
    method = fetch(session, Method, item.method_id)
    require_scope(user, "sources", item.source_id)
    require_scope(user, "indicators", method.indicator_id)
    result = json.loads(item.result_json)
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(
        [
            "run_id",
            "indicator_id",
            "method_id",
            "version",
            "source_id",
            "source_sha256",
            "engine",
            "period",
            "group",
            "value",
            "unit",
            "status",
            "rows",
        ]
    )

    def safe(value):
        text = str(value) if value is not None else ""
        return "'" + text if text.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")) else text

    for point in result["series"]:
        writer.writerow(
            [
                safe(v)
                for v in (
                    item.id,
                    method.indicator_id,
                    method.id,
                    method.version,
                    item.source_id,
                    result["source_sha256"],
                    item.engine_version,
                    point["period"],
                    point["group"],
                    point["value"],
                    result["unit"],
                    point["status"],
                    point["rows"],
                )
            ]
        )
    audit(session, user, "run.export", item.id)
    session.commit()
    return Response(
        "\ufeff" + output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="sii-mb-{item.id}.csv"'},
    )


@router.post("/runs/{run_id}/reproduce", status_code=201)
def reproduce(run_id: str, session: Session = Depends(get_db), user: User = Depends(editor)):
    old = fetch(session, Run, run_id)
    if old.engine_version != ENGINE_VERSION:
        raise HTTPException(409, "Esta versión del motor requiere su entorno histórico")
    payload = RunInput.model_validate_json(old.request_json)
    return execute(payload, session, user)
