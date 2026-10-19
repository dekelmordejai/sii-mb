from datetime import datetime, timezone

from sqlalchemy import Boolean, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


class Base(DeclarativeBase):
    pass


class Indicator(Base):
    """Catalog entity only. No formulas or institutional approvals at this milestone."""

    __tablename__ = "indicators"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="draft")
    created_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now_iso)
    updated_at: Mapped[str] = mapped_column(String(40), nullable=False, default=utc_now_iso)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    dimensions_json: Mapped[str] = mapped_column(Text, default="[]")

    @property
    def dimensions(self):
        import json

        return json.loads(self.dimensions_json)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(20))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    scopes_json: Mapped[str] = mapped_column(Text, default='{"indicators": [], "sources": []}')
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[float] = mapped_column(Float)


class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    failures: Mapped[int] = mapped_column(default=0)
    blocked_until: Mapped[float] = mapped_column(Float, default=0)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    actor_id: Mapped[str] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(80))
    object_id: Mapped[str] = mapped_column(String(80))
    detail_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)


class IndicatorRelation(Base):
    __tablename__ = "indicator_relations"
    __table_args__ = (UniqueConstraint("source_id", "target_id", "label"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("indicators.id"))
    target_id: Mapped[str] = mapped_column(ForeignKey("indicators.id"))
    label: Mapped[str] = mapped_column(String(100))


class Dashboard(Base):
    __tablename__ = "dashboards"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(160))
    config_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    kind: Mapped[str] = mapped_column(String(20), default="csv")
    sha256: Mapped[str] = mapped_column(String(64))
    content: Mapped[str] = mapped_column(Text)
    profile_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)


class Method(Base):
    __tablename__ = "methods"
    __table_args__ = (UniqueConstraint("indicator_id", "version"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    indicator_id: Mapped[str] = mapped_column(ForeignKey("indicators.id"))
    version: Mapped[int]
    config_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    method_id: Mapped[str] = mapped_column(ForeignKey("methods.id"))
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"))
    request_json: Mapped[str] = mapped_column(Text)
    result_json: Mapped[str] = mapped_column(Text)
    engine_version: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[str] = mapped_column(String(40), default=utc_now_iso)
