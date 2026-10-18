import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD", "synthetic-test-pass-2026")
    app = create_app("sqlite+pysqlite:///:memory:")
    with TestClient(app) as http:
        assert http.post("/api/v1/auth/login", json={"username": "admin", "password": "synthetic-test-pass-2026"}).status_code == 200
        yield http
