from uuid import UUID


def example_payload():
    return {
        "name": "Intervalo observado (demostración)",
        "definition": "Tiempo transcurrido entre dos pasos sucesivos en una parada.",
        "domain": "Operación",
        "unit": "min",
    }


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["environment"] == "local-development"


def test_empty_catalog(client):
    response = client.get("/api/v1/indicators")
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0, "limit": 30, "offset": 0}


def test_create_get_and_patch_draft(client):
    created = client.post("/api/v1/indicators", json=example_payload())
    assert created.status_code == 201, created.text
    item = created.json()
    UUID(item["id"])
    assert item["status"] == "draft"
    assert item["code"].startswith("IND-")
    assert client.get(f'/api/v1/indicators/{item["id"]}').json() == item
    modified = client.patch(f'/api/v1/indicators/{item["id"]}', json={"unit": "seg"})
    assert modified.status_code == 200
    assert modified.json()["unit"] == "seg"
    assert modified.json()["code"] == item["code"]


def test_invalid_input_and_server_controlled_status(client):
    bad = example_payload() | {"name": "A"}
    assert client.post("/api/v1/indicators", json=bad).status_code == 422
    bad_status = example_payload() | {"status": "approved"}
    assert client.post("/api/v1/indicators", json=bad_status).status_code == 422


def test_search_and_pagination(client):
    for name in ["Intervalo de autobuses", "Demanda de viajes", "Flota operativa"]:
        payload = example_payload() | {"name": name}
        assert client.post("/api/v1/indicators", json=payload).status_code == 201
    found = client.get("/api/v1/indicators?q=intervalo")
    assert found.status_code == 200
    assert found.json()["total"] == 1
    page = client.get("/api/v1/indicators?limit=2&offset=2").json()
    assert page["total"] == 3
    assert len(page["items"]) == 1


def test_missing_indicator(client):
    assert client.get("/api/v1/indicators/no-existe").status_code == 404
    assert client.patch("/api/v1/indicators/no-existe", json={"unit": "km"}).status_code == 404


def test_patch_rejects_unknown_fields_and_nulls(client):
    created = client.post("/api/v1/indicators", json=example_payload()).json()
    url = f'/api/v1/indicators/{created["id"]}'
    assert client.patch(url, json={"status": "approved"}).status_code == 422
    assert client.patch(url, json={"name": None}).status_code == 422


def test_file_persistence_across_app_restarts(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import create_app

    database = tmp_path / "local.db"
    monkeypatch.setenv("SII_MB_ADMIN_PASSWORD", "synthetic-test-pass-2026")
    url = f"sqlite+pysqlite:///{database}"
    with TestClient(create_app(url)) as first:
        first.post("/api/v1/auth/login", json={"username": "admin", "password": "synthetic-test-pass-2026"})
        res = first.post("/api/v1/indicators", json=example_payload())
        assert res.status_code == 201
        identifier = res.json()["id"]
    with TestClient(create_app(url)) as second:
        second.post("/api/v1/auth/login", json={"username": "admin", "password": "synthetic-test-pass-2026"})
        assert second.get(f"/api/v1/indicators/{identifier}").status_code == 200
        assert second.get("/api/v1/indicators").json()["total"] == 1
