import os
from collections.abc import Iterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from sqlalchemy import create_engine, event, select
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


def default_database_url() -> str:
    # Relative to backend/, independent of where uvicorn was launched.
    data_path = Path(__file__).resolve().parents[1] / "data" / "sii_mb.db"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+pysqlite:///{data_path}"


def make_engine(database_url: str) -> Engine:
    options: dict = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        filename = make_url(database_url).database
        if filename and filename != ":memory:":
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
        options["connect_args"] = {"check_same_thread": False}
        if database_url.endswith(":memory:"):
            options["poolclass"] = StaticPool
    engine = create_engine(database_url, **options)
    if database_url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

    return engine


def make_lifespan(database_url: str | None):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        url = database_url or os.getenv("SII_MB_DATABASE_URL") or default_database_url()
        engine = make_engine(url)
        from app.migrations import upgrade
        from app.models import User
        from app.security import bootstrap

        upgrade(engine)
        app.state.session_factory = sessionmaker(bind=engine, expire_on_commit=False)
        if os.getenv("SII_MB_ADMIN_PASSWORD"):
            with app.state.session_factory() as session:
                if session.scalar(select(User.id).limit(1)) is None:
                    bootstrap(
                        session,
                        os.getenv("SII_MB_ADMIN_USERNAME", "admin"),
                        os.environ["SII_MB_ADMIN_PASSWORD"],
                    )
        try:
            yield
        finally:
            engine.dispose()

    return lifespan


def get_db(request: Request) -> Iterator[Session]:
    factory = request.app.state.session_factory
    with factory() as session:
        yield session
