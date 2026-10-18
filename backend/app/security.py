import hashlib
import hmac
import json
import os
import secrets
import time
from uuid import uuid4

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import AuditEvent, LoginSession, User

COOKIE = "sii_mb_session"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1)
    return salt.hex() + ":" + digest.hex()


def verify_password(password: str, encoded: str) -> bool:
    salt, digest = encoded.split(":")
    return hmac.compare_digest(hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex(), digest)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def current_user(request: Request, session: Session = Depends(get_db)) -> User:
    record = session.get(LoginSession, token_hash(request.cookies.get(COOKIE, "")))
    if not record or record.expires_at < time.time():
        raise HTTPException(401, "Inicia sesión para continuar")
    user = session.get(User, record.user_id)
    if not user or not user.active:
        raise HTTPException(401, "Cuenta desactivada")
    return user


def editor(user: User = Depends(current_user)) -> User:
    if user.role not in ("admin", "editor"):
        raise HTTPException(403, "Se requiere permiso de edición")
    return user


def admin(user: User = Depends(current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Se requiere administración")
    return user


def allowed(user: User, kind: str, identifier: str) -> bool:
    scope = json.loads(user.scopes_json).get(kind, [])
    return user.role == "admin" or "*" in scope or identifier in scope


def require_scope(user: User, kind: str, identifier: str):
    if not allowed(user, kind, identifier):
        raise HTTPException(403, "El registro está fuera de tu alcance autorizado")


def grant_created(user: User, kind: str, identifier: str):
    scopes = json.loads(user.scopes_json)
    scopes.setdefault(kind, []).append(identifier)
    user.scopes_json = json.dumps(scopes)


def audit(session: Session, actor: User, action: str, object_id: str, detail=None):
    session.add(AuditEvent(id=str(uuid4()), actor_id=actor.id, action=action, object_id=object_id, detail_json=json.dumps(detail or {}, ensure_ascii=False)))


def public_user(user: User):
    return {"id": user.id, "username": user.username, "role": user.role, "active": user.active, "scopes": json.loads(user.scopes_json)}


def bootstrap(session: Session, username: str, password: str):
    if len(password) < 12 or len(password) > 128:
        raise ValueError("La contraseña debe tener entre 12 y 128 caracteres")
    user = User(id=str(uuid4()), username=username.lower(), password_hash=hash_password(password), role="admin")
    session.add(user)
    audit(session, user, "admin.bootstrap", user.id)
    session.commit()
    return user
