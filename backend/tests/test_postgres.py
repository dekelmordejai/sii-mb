"""Opt-in integration against a dedicated local test database."""

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.mark.skipif(
    not os.getenv("SII_MB_TEST_POSTGRES_URL"), reason="Requires PostgreSQL row locking"
)
def test_concurrent_editor_creation_keeps_all_scope_grants(client):
    from tests.test_core import login_as

    created = client.post(
        "/api/v1/users",
        json={
            "username": "concurrent-editor",
            "password": "synthetic-password-2026",
            "role": "editor",
        },
    )
    assert created.status_code == 201
    login_as(client, "concurrent-editor")

    def create(index):
        return client.post(
            "/api/v1/indicators",
            json={
                "name": f"Sintético paralelo {index}",
                "definition": "Indicador sintético para validar concurrencia",
                "unit": "u",
            },
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(create, range(12)))
    assert all(r.status_code == 201 for r in responses), [
        r.text for r in responses if r.status_code != 201
    ]
    identifiers = {r.json()["id"] for r in responses}
    assert set(client.get("/api/v1/auth/me").json()["scopes"]["indicators"]) == identifiers
    assert client.get("/api/v1/indicators").json()["total"] == 12


@pytest.mark.skipif(
    not os.getenv("SII_MB_TEST_POSTGRES_URL"),
    reason="Requires dedicated local PostgreSQL test database",
)
def test_postgres_migrations_calculation_and_restart(monkeypatch):
    from tests.test_core import execute, setup

    base = sa.engine.make_url(os.environ["SII_MB_TEST_POSTGRES_URL"])
    schema = "test_sii_" + uuid4().hex
    engine = sa.create_engine(base)
    with engine.begin() as connection:
        connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
    url = base.update_query_dict({"options": f"-csearch_path={schema}"}).render_as_string(
        hide_password=False
    )
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD", "synthetic-test-pass-2026")
    try:
        with TestClient(create_app(url)) as client:
            client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "synthetic-test-pass-2026"},
            )
            indicator, source, method = setup(client)
            run = execute(client, source, method)
            assert run.status_code == 201, run.text
            run = run.json()
        with TestClient(create_app(url)) as client:
            client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "synthetic-test-pass-2026"},
            )
            assert client.get(f"/api/v1/runs/{run['id']}").json() == run
    finally:
        with engine.begin() as connection:
            connection.execute(sa.text(f'DROP SCHEMA "{schema}" CASCADE'))
        engine.dispose()


@pytest.mark.skipif(
    not os.getenv("SII_MB_TEST_POSTGRES_URL") or not os.getenv("SII_MB_PG_BIN"),
    reason="Requires PostgreSQL test database and matching pg_dump/pg_restore binaries",
)
def test_postgres_backup_restore_preserves_history(tmp_path, monkeypatch):
    from tests.test_core import execute, setup

    base = sa.engine.make_url(os.environ["SII_MB_TEST_POSTGRES_URL"])
    schema = "test_sii_" + uuid4().hex
    restored_database = "test_sii_restore_" + uuid4().hex
    engine = sa.create_engine(base)
    pg_bin = Path(os.environ["SII_MB_PG_BIN"])
    executable_suffix = ".exe" if os.name == "nt" else ""
    env = os.environ | {
        "PGHOST": base.host,
        "PGPORT": str(base.port or 5432),
        "PGUSER": base.username,
        "PGPASSWORD": base.password or "",
        "PGDATABASE": base.database,
    }
    url = base.update_query_dict({"options": f"-csearch_path={schema}"}).render_as_string(
        hide_password=False
    )
    restored_url = (
        base.set(database=restored_database)
        .update_query_dict({"options": f"-csearch_path={schema}"})
        .render_as_string(hide_password=False)
    )
    with engine.begin() as connection:
        connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD", "synthetic-test-pass-2026")
    database_created = False
    try:
        with TestClient(create_app(url)) as client:
            client.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "synthetic-test-pass-2026"},
            )
            _, source, method = setup(client)
            run = execute(client, source, method).json()
        backup = tmp_path / "synthetic-backup.dump"
        subprocess.run(
            [
                str(pg_bin / ("pg_dump" + executable_suffix)),
                "--format=custom",
                "--schema",
                schema,
                "--file",
                str(backup),
            ],
            env=env,
            check=True,
            capture_output=True,
        )
        assert backup.stat().st_size > 0
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(sa.text(f'CREATE DATABASE "{restored_database}"'))
        database_created = True
        subprocess.run(
            [
                str(pg_bin / ("pg_restore" + executable_suffix)),
                "--no-owner",
                "--exit-on-error",
                "--dbname",
                restored_database,
                str(backup),
            ],
            env=env,
            check=True,
            capture_output=True,
        )
        with TestClient(create_app(restored_url)) as client:
            assert (
                client.post(
                    "/api/v1/auth/login",
                    json={"username": "admin", "password": "synthetic-test-pass-2026"},
                ).status_code
                == 200
            )
            assert client.get(f"/api/v1/runs/{run['id']}").json() == run
            assert (
                client.post(f"/api/v1/runs/{run['id']}/reproduce").json()["result"] == run["result"]
            )
    finally:
        if database_created:
            with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(sa.text(f'DROP DATABASE "{restored_database}"'))
        with engine.begin() as connection:
            connection.execute(sa.text(f'DROP SCHEMA "{schema}" CASCADE'))
        engine.dispose()
