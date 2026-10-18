import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    app = create_app("sqlite+pysqlite:///:memory:")
    with TestClient(app) as http:
        yield http
