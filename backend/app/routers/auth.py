import json
import os
import secrets
import time
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import AuditEvent, LoginAttempt, LoginSession, User
from app.security import (
    COOKIE,
    admin,
    audit,
    current_user,
    hash_password,
    public_user,
    token_hash,
    verify_password,
)

router = APIRouter(prefix="/api/v1", tags=["identity"])


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=128)


class Scopes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    indicators: list[str] = Field(default_factory=list, max_length=1000)
    sources: list[str] = Field(default_factory=list, max_length=1000)


class UserInput(LoginInput):
    username: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=12, max_length=128)
    role: Literal["admin", "editor", "viewer"]
    scopes: Scopes = Field(default_factory=Scopes)


class UserPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    active: bool
    role: Literal["admin", "editor", "viewer"]
    scopes: Scopes
    password: str | None = Field(default=None, min_length=12, max_length=128)


@router.post("/auth/login")
def login(
    payload: LoginInput,
    request: Request,
    response: Response,
    session: Session = Depends(get_db),
):
    username = payload.username.lower()
    key = token_hash(username)
    attempt = session.get(LoginAttempt, key)
    now = time.time()
    if attempt and attempt.blocked_until > now:
        raise HTTPException(429, "Demasiados intentos; espera 15 minutos")
    if attempt and attempt.blocked_until and attempt.blocked_until <= now:
        attempt.failures = 0
        attempt.blocked_until = 0
    user = session.scalar(select(User).where(User.username == username))
    # Fixed dummy salt/digest performs the same expensive check for unknown accounts.
    encoded = user.password_hash if user else "00" * 16 + ":" + "00" * 64
    valid = verify_password(payload.password, encoded)
    if not user or not user.active or not valid:
        if not attempt:
            attempt = LoginAttempt(key=key, failures=0, blocked_until=0)
            session.add(attempt)
        attempt.failures += 1
        if attempt.failures >= 5:
            attempt.blocked_until = now + 900
        if user:
            audit(session, user, "auth.login_failed", user.id)
        session.commit()
        raise HTTPException(401, "Usuario o contraseña incorrectos")
    if attempt:
        session.delete(attempt)
    token = secrets.token_urlsafe(32)
    session.add(
        LoginSession(token_hash=token_hash(token), user_id=user.id, expires_at=now + 8 * 3600)
    )
    session.execute(delete(LoginSession).where(LoginSession.expires_at < now))
    audit(session, user, "auth.login", user.id)
    session.commit()
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        samesite="strict",
        secure=os.getenv("SII_MB_SECURE_COOKIES") == "1",
        max_age=8 * 3600,
        path="/",
    )
    return public_user(user)


@router.get("/auth/me")
def me(user: User = Depends(current_user)):
    return public_user(user)


@router.post("/auth/logout")
def logout(
    request: Request,
    response: Response,
    user: User = Depends(current_user),
    session: Session = Depends(get_db),
):
    session.execute(
        delete(LoginSession).where(
            LoginSession.token_hash == token_hash(request.cookies.get(COOKIE, ""))
        )
    )
    audit(session, user, "auth.logout", user.id)
    session.commit()
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@router.get("/users")
def users(user: User = Depends(admin), session: Session = Depends(get_db)):
    return [public_user(u) for u in session.scalars(select(User).order_by(User.username))]


@router.post("/users", status_code=201)
def create_user(
    payload: UserInput, actor: User = Depends(admin), session: Session = Depends(get_db)
):
    if session.scalar(select(User).where(User.username == payload.username.lower())):
        raise HTTPException(409, "El usuario ya existe")
    item = User(
        id=str(uuid4()),
        username=payload.username.lower(),
        password_hash=hash_password(payload.password),
        role=payload.role,
        scopes_json=payload.scopes.model_dump_json(),
    )
    session.add(item)
    audit(
        session,
        actor,
        "user.create",
        item.id,
        {"role": item.role, "scopes": payload.scopes.model_dump()},
    )
    session.commit()
    return public_user(item)


@router.patch("/users/{user_id}")
def update_user(
    user_id: str,
    payload: UserPatch,
    actor: User = Depends(admin),
    session: Session = Depends(get_db),
):
    item = session.get(User, user_id)
    if not item:
        raise HTTPException(404, "Usuario no encontrado")
    if item.id == actor.id and (not payload.active or payload.role != "admin"):
        raise HTTPException(409, "No puedes quitar tu propio acceso administrativo")
    item.active, item.role, item.scopes_json = (
        payload.active,
        payload.role,
        payload.scopes.model_dump_json(),
    )
    if payload.password:
        item.password_hash = hash_password(payload.password)
    session.execute(delete(LoginSession).where(LoginSession.user_id == item.id))
    audit(session, actor, "user.update", item.id, payload.model_dump(exclude={"password"}))
    session.commit()
    return public_user(item)


@router.get("/audit")
def events(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: User = Depends(admin),
    session: Session = Depends(get_db),
):
    return {
        "items": [
            {
                "id": e.id,
                "actor_id": e.actor_id,
                "action": e.action,
                "object_id": e.object_id,
                "detail": json.loads(e.detail_json),
                "created_at": e.created_at,
            }
            for e in session.scalars(
                select(AuditEvent)
                .order_by(AuditEvent.created_at.desc(), AuditEvent.id)
                .limit(limit)
                .offset(offset)
            )
        ],
        "total": session.scalar(select(func.count()).select_from(AuditEvent)),
    }
