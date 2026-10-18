"""Opt-in integration against a dedicated local test database."""
import os
from uuid import uuid4
import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.mark.skipif(not os.getenv("SII_MB_TEST_POSTGRES_URL"), reason="Requires dedicated local PostgreSQL test database")
def test_postgres_migrations_calculation_and_restart(monkeypatch):
    from tests.test_core import setup, execute
    base=sa.engine.make_url(os.environ["SII_MB_TEST_POSTGRES_URL"])
    schema="test_sii_"+uuid4().hex
    engine=sa.create_engine(base)
    with engine.begin() as connection:
        connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
    url=base.update_query_dict({"options":f"-csearch_path={schema}"}).render_as_string(hide_password=False)
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD","synthetic-test-pass-2026")
    try:
        with TestClient(create_app(url)) as client:
            client.post("/api/v1/auth/login",json={"username":"admin","password":"synthetic-test-pass-2026"})
            indicator,source,method=setup(client)
            run=execute(client,source,method)
            assert run.status_code==201,run.text
            run=run.json()
        with TestClient(create_app(url)) as client:
            client.post("/api/v1/auth/login",json={"username":"admin","password":"synthetic-test-pass-2026"})
            assert client.get(f'/api/v1/runs/{run["id"]}').json()==run
    finally:
        with engine.begin() as connection:
            connection.execute(sa.text(f'DROP SCHEMA "{schema}" CASCADE'))
        engine.dispose()
