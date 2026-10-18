import json
from typing import Literal
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Dashboard, Indicator, IndicatorRelation, Method, Run, User
from app.routers.analysis import fetch, run_view
from app.security import allowed, audit, current_user, editor, require_scope

router = APIRouter(prefix="/api/v1", tags=["workspace"])


class Widget(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str = Field(min_length=1, max_length=36)
    title: str = Field(min_length=1, max_length=160)
    chart: Literal["line", "bar", "table", "kpi"] = "line"


class DashboardInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=3, max_length=160)
    widgets: list[Widget] = Field(min_length=1, max_length=12)


def dashboard_view(item, session, user):
    widgets = json.loads(item.config_json)
    for widget in widgets:
        record = fetch(session, Run, widget["run_id"])
        require_scope(user, "sources", record.source_id)
        require_scope(user, "indicators", fetch(session, Method, record.method_id).indicator_id)
    return {"id": item.id, "name": item.name, "owner_id": item.owner_id, "widgets": widgets, "created_at": item.created_at}


@router.get("/dashboards")
def dashboards(session: Session = Depends(get_db), user: User = Depends(current_user)):
    items = session.scalars(select(Dashboard).where(Dashboard.owner_id == user.id).order_by(Dashboard.created_at.desc()))
    visible = []
    for item in items:
        try:
            visible.append(dashboard_view(item, session, user))
        except HTTPException as exc:
            if exc.status_code != 403:
                raise
    return visible


@router.post("/dashboards", status_code=201)
def create_dashboard(payload: DashboardInput, session: Session = Depends(get_db), user: User = Depends(editor)):
    item = Dashboard(id=str(uuid4()), owner_id=user.id, name=payload.name, config_json=json.dumps([w.model_dump() for w in payload.widgets]))
    dashboard_view(item, session, user)
    session.add(item)
    audit(session, user, "dashboard.create", item.id, payload.model_dump())
    session.commit()
    return dashboard_view(item, session, user)


@router.patch("/dashboards/{dashboard_id}")
def update_dashboard(dashboard_id: str, payload: DashboardInput, session: Session = Depends(get_db), user: User = Depends(editor)):
    item = fetch(session, Dashboard, dashboard_id)
    if item.owner_id != user.id:
        raise HTTPException(403, "Solo la persona creadora puede editar este tablero")
    item.name, item.config_json = payload.name, json.dumps([w.model_dump() for w in payload.widgets])
    dashboard_view(item, session, user)
    audit(session, user, "dashboard.update", item.id, payload.model_dump())
    session.commit()
    return dashboard_view(item, session, user)


class RelationInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    target_id: str = Field(max_length=36)
    label: str = Field(min_length=3, max_length=100)


@router.post("/indicators/{indicator_id}/relations", status_code=201)
def create_relation(indicator_id: str, payload: RelationInput, session: Session = Depends(get_db), user: User = Depends(editor)):
    for identifier in (indicator_id, payload.target_id):
        require_scope(user, "indicators", identifier)
        fetch(session, Indicator, identifier)
    if indicator_id == payload.target_id:
        raise HTTPException(422, "Selecciona otro indicador")
    item = IndicatorRelation(id=str(uuid4()), source_id=indicator_id, target_id=payload.target_id, label=payload.label)
    session.add(item)
    audit(session, user, "indicator.relate", indicator_id, payload.model_dump())
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "La relación ya existe") from None
    return {"id": item.id, "source_id": indicator_id, **payload.model_dump()}


@router.get("/indicators/{indicator_id}/relations")
def relations(indicator_id: str, session: Session = Depends(get_db), user: User = Depends(current_user)):
    require_scope(user, "indicators", indicator_id)
    return [{"id": r.id, "source_id": r.source_id, "target_id": r.target_id, "label": r.label}
            for r in session.scalars(select(IndicatorRelation).where(or_(IndicatorRelation.source_id == indicator_id, IndicatorRelation.target_id == indicator_id)))
            if allowed(user, "indicators", r.source_id) and allowed(user, "indicators", r.target_id)]
