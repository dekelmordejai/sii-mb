import os
from uuid import uuid4

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def test_database_url():
    if not os.getenv("SII_MB_TEST_POSTGRES_URL"):
        yield "sqlite+pysqlite:///:memory:"
        return
    base = sa.engine.make_url(os.environ["SII_MB_TEST_POSTGRES_URL"])
    schema = "test_sii_" + uuid4().hex
    engine = sa.create_engine(base)
    with engine.begin() as connection:
        connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
    try:
        yield base.update_query_dict({"options": f"-csearch_path={schema}"}).render_as_string(
            hide_password=False
        )
    finally:
        with engine.begin() as connection:
            connection.execute(sa.text(f'DROP SCHEMA "{schema}" CASCADE'))
        engine.dispose()


@pytest.fixture
def client(monkeypatch, test_database_url):
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD", "synthetic-test-pass-2026")
    app = create_app(test_database_url)
    with TestClient(app) as http:
        assert (
            http.post(
                "/api/v1/auth/login",
                json={"username": "admin", "password": "synthetic-test-pass-2026"},
            ).status_code
            == 200
        )
        yield http
