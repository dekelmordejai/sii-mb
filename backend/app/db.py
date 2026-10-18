import os
from collections.abc import Iterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.models import Base


def default_database_url() -> str:
    # Relative to backend/, independent of where uvicorn was launched.
    data_path = Path(__file__).resolve().parents[1] / "data" / "sii_mb.db"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+pysqlite:///{data_path}"


def make_engine(database_url: str) -> Engine:
    options: dict = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
        if database_url.endswith(":memory:"):
            options["poolclass"] = StaticPool
    return create_engine(database_url, **options)


def make_lifespan(database_url: str | None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        url = database_url or os.getenv("SII_MB_DATABASE_URL") or default_database_url()
        engine = make_engine(url)
        Base.metadata.create_all(bind=engine)  # MVP only; switch to Alembic in M2.
        app.state.session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        try:
            yield
        finally:
            engine.dispose()

    return lifespan


def get_db(request: Request) -> Iterator[Session]:
    factory = request.app.state.session_factory
    with factory() as session:
        yield session
