from decimal import Decimal

import pytest

from app.calculation import MethodConfig, RunInput, calculate

CSV = "fecha,grupo,valor,base\n2026-01-01,A,80,100\n2026-01-01,B,30,50\n2026-01-02,A,90,100\n2026-01-02,B,45,50\n"


def setup(client, content=CSV, config=None):
    source = client.post("/api/v1/sources", json={"name": "Fuente sintética", "content": content})
    assert source.status_code == 201, source.text
    indicator = client.post(
        "/api/v1/indicators",
        json={
            "name": "Indicador ficticio",
            "definition": "Datos ficticios para verificar la plataforma",
            "unit": "%",
            "dimensions": ["fecha", "grupo"],
        },
    ).json()
    method = client.post(
        f"/api/v1/indicators/{indicator['id']}/methods",
        json=config
        or {
            "operation": "ratio_of_sums",
            "numerator": "valor",
            "denominator": "base",
            "multiplier": 100,
            "unit": "%",
            "date_column": "fecha",
            "group_by": "grupo",
        },
    )
    assert method.status_code == 201, method.text
    return indicator, source.json(), method.json()


def execute(client, source, method, **kwargs):
    return client.post(
        "/api/v1/runs",
        json={"method_id": method["id"], "source_id": source["id"], **kwargs},
    )


def test_vertical_versioning_reproduction_and_dashboard(client):
    indicator, source, method = setup(client)
    run = execute(client, source, method)
    assert run.status_code == 201, run.text
    run = run.json()
    assert Decimal(run["result"]["total"]["value"]).quantize(Decimal("0.000001")) == Decimal(
        "81.666667"
    )
    assert run["result"]["result_status"] == "provisional"
    assert run["result"]["usage_authorization"] == "none"
    assert run["result"]["source_sha256"] == source["sha256"]
    repeated = client.post(f"/api/v1/runs/{run['id']}/reproduce").json()
    assert repeated["id"] != run["id"]
    assert repeated["result"] == run["result"]
    new_method = client.post(
        f"/api/v1/indicators/{indicator['id']}/methods",
        json={"operation": "mean", "numerator": "valor", "unit": "unidades"},
    ).json()
    assert new_method["version"] == 2
    assert execute(client, source, new_method).json()["result"]["total"]["value"] == "61.25"
    assert client.get(f"/api/v1/runs/{run['id']}").json() == run
    dashboard = client.post(
        "/api/v1/dashboards",
        json={
            "name": "Tablero sintético",
            "widgets": [{"run_id": run["id"], "title": "Prueba", "chart": "line"}],
        },
    )
    assert dashboard.status_code == 201, dashboard.text
    assert client.get("/api/v1/dashboards").json()[0]["widgets"][0]["run_id"] == run["id"]
    assert (
        client.patch(
            f"/api/v1/dashboards/{dashboard.json()['id']}",
            json={
                "name": "Tablero actualizado",
                "widgets": [{"run_id": run["id"], "title": "Resumen", "chart": "kpi"}],
            },
        ).status_code
        == 200
    )
    exported = client.get(f"/api/v1/runs/{run['id']}/export")
    assert exported.status_code == 200
    assert source["sha256"] in exported.text
    assert "period,group,value" in exported.text


def test_filters_and_zero_denominator(client):
    _, source, method = setup(client)
    run = execute(
        client,
        source,
        method,
        filters={"grupo": "A"},
        start="2026-01-02",
        end="2026-01-02",
    ).json()
    assert run["result"]["total"]["value"] == "90.0"
    assert run["result"]["selected_rows"] == 1
    assert execute(client, source, method, filters={"unknown": "x"}).status_code == 422
    assert execute(client, source, method, start="2026-02-01", end="2026-01-01").status_code == 422
    _, zero, zm = setup(client, "fecha,grupo,valor,base\n2026-01-01,A,1,0\n")
    result = execute(client, zero, zm).json()["result"]
    assert result["total"]["value"] is None
    assert result["total"]["status"] == "zero_denominator"


@pytest.mark.parametrize("content", ["", "a,a\n1,2", "a,b\n1", 'a,b\n"open,2', "a\n\x00"])
def test_invalid_csv_rejected(client, content):
    assert (
        client.post("/api/v1/sources", json={"name": "Prueba", "content": content}).status_code
        == 422
    )


def test_schema_and_missing_values(client):
    assert (
        client.post(
            "/api/v1/sources",
            json={"name": "Prueba", "content": "a\ntext", "types": {"a": "number"}},
        ).status_code
        == 422
    )
    _, source, method = setup(
        client, "fecha,grupo,valor,base\n2026-01-01,A,,10\n2026-01-02,A,5,10\n"
    )
    assert execute(client, source, method).status_code == 422
    config = MethodConfig(operation="sum", numerator="valor", unit="u", missing="skip")
    request = RunInput(method_id="m", source_id="s")
    result = calculate('valor\n""\n5\n', config, request)
    assert result["total"]["value"] == "5" and result["skipped_missing"] == 1
    config.missing = "zero"
    assert calculate('valor\n""\n5\n', config, request)["selected_rows"] == 2


@pytest.mark.parametrize(
    "value", ["NaN", "Infinity", "-Infinity", "1e1000", "1e-1000", "__import__('os')"]
)
def test_non_finite_or_code_rejected(client, value):
    _, source, method = setup(client, f"fecha,grupo,valor,base\n2026-01-01,A,{value},10\n")
    assert execute(client, source, method).status_code == 422


def test_safe_composite_expression_and_conditions(client):
    expr = {
        "op": "multiply",
        "args": [
            {
                "op": "divide",
                "args": [
                    {
                        "op": "sum",
                        "column": "valor",
                        "where": {"column": "grupo", "eq": "A"},
                    },
                    {
                        "op": "sum",
                        "column": "base",
                        "where": {"column": "grupo", "eq": "A"},
                    },
                ],
            },
            {"op": "literal", "value": 100},
        ],
    }
    indicator, source, method = setup(
        client, config={"operation": "expression", "expression": expr, "unit": "%"}
    )
    assert execute(client, source, method).json()["result"]["total"]["value"] == "85.00"
    for expr in [
        {"op": "eval", "code": "print(1)"},
        {"op": "divide", "args": []},
        {"op": "sum", "column": "valor", "sql": "DROP TABLE"},
    ]:
        res = client.post(
            f"/api/v1/indicators/{indicator['id']}/methods",
            json={"operation": "expression", "expression": expr, "unit": "%"},
        )
        assert res.status_code == 422


def test_month_and_validity():
    config = MethodConfig(
        operation="sum",
        numerator="valor",
        unit="u",
        date_column="fecha",
        granularity="month",
        valid_from="2026-01-02",
    )
    result = calculate(CSV, config, RunInput(method_id="m", source_id="s"))
    assert result["series"][0]["period"] == "2026-01"
    assert result["total"]["value"] == "135"


@pytest.mark.parametrize(
    "operation,expected", [("count", "4"), ("min", "30"), ("max", "90"), ("sum", "245")]
)
def test_basic_aggregates(operation, expected):
    config = MethodConfig(
        operation=operation, numerator=None if operation == "count" else "valor", unit="u"
    )
    assert (
        calculate(CSV, config, RunInput(method_id="m", source_id="s"))["total"]["value"] == expected
    )


def login_as(client, name, password="synthetic-password-2026"):
    client.post("/api/v1/auth/logout")
    assert (
        client.post("/api/v1/auth/login", json={"username": name, "password": password}).status_code
        == 200
    )


def test_roles_scopes_and_export_security(client):
    indicator, source, method = setup(client)
    run = execute(client, source, method).json()
    viewer = client.post(
        "/api/v1/users",
        json={
            "username": "viewer",
            "password": "synthetic-password-2026",
            "role": "viewer",
            "scopes": {"indicators": [indicator["id"]], "sources": []},
        },
    )
    assert viewer.status_code == 201
    login_as(client, "viewer")
    assert client.get("/api/v1/indicators").json()["total"] == 1
    assert client.get("/api/v1/sources").json()["total"] == 0
    assert client.get("/api/v1/runs").json()["total"] == 0
    assert client.get(f"/api/v1/runs/{run['id']}").status_code == 403
    assert client.get(f"/api/v1/runs/{run['id']}/export").status_code == 403
    assert execute(client, source, method).status_code == 403
    assert (
        client.post("/api/v1/sources", json={"name": "Source", "content": "a\n1"}).status_code
        == 403
    )
    assert client.get("/api/v1/users").status_code == 403
    assert client.get("/api/v1/audit").status_code == 403
    assert (
        client.patch(f"/api/v1/indicators/{indicator['id']}", json={"name": "Changed"}).status_code
        == 403
    )


def test_editor_scope_is_enforced_and_own_creation_grants_scope(client):
    indicator, source, method = setup(client)
    client.post(
        "/api/v1/users",
        json={
            "username": "editor",
            "password": "synthetic-password-2026",
            "role": "editor",
        },
    )
    login_as(client, "editor")
    assert client.get(f"/api/v1/indicators/{indicator['id']}").status_code == 403
    assert execute(client, source, method).status_code == 403
    own, own_source, own_method = setup(client)
    assert client.get(f"/api/v1/indicators/{own['id']}").status_code == 200
    assert execute(client, own_source, own_method).status_code == 201


def test_login_logout_csrf_and_rate_limit(client):
    assert client.post("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/indicators").status_code == 401
    assert (
        client.post(
            "/api/v1/auth/login",
            headers={"Origin": "https://evil.example"},
            json={"username": "admin", "password": "synthetic-test-pass-2026"},
        ).status_code
        == 403
    )
    for _ in range(5):
        assert (
            client.post(
                "/api/v1/auth/login", json={"username": "admin", "password": "wrong"}
            ).status_code
            == 401
        )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "synthetic-test-pass-2026"},
        ).status_code
        == 429
    )


def test_deactivate_relations_and_audit(client):
    indicator, source, method = setup(client)
    other, _, _ = setup(client)
    rel = client.post(
        f"/api/v1/indicators/{indicator['id']}/relations",
        json={"target_id": other["id"], "label": "Comparación sintética"},
    )
    assert rel.status_code == 201
    assert len(client.get(f"/api/v1/indicators/{indicator['id']}/relations").json()) == 1
    assert (
        client.patch(f"/api/v1/indicators/{indicator['id']}", json={"active": False}).status_code
        == 200
    )
    assert execute(client, source, method).status_code == 409
    assert client.get(f"/api/v1/indicators/{indicator['id']}").json()["status"] == "draft"
    actions = [e["action"] for e in client.get("/api/v1/audit?limit=200").json()["items"]]
    assert {
        "indicator.create",
        "indicator.update",
        "indicator.relate",
        "method.create",
        "source.create",
    }.issubset(actions)


def test_csv_export_escapes_spreadsheet_formulas(client):
    _, source, method = setup(client, "fecha,grupo,valor,base\n2026-01-01,=1+1,5,10\n")
    run = execute(client, source, method).json()
    assert "'=1+1" in client.get(f"/api/v1/runs/{run['id']}/export").text


def test_account_revocation_and_last_admin(client):
    me = client.get("/api/v1/auth/me").json()
    assert (
        client.patch(
            f"/api/v1/users/{me['id']}",
            json={"active": False, "role": "viewer", "scopes": {}},
        ).status_code
        == 409
    )
    created = client.post(
        "/api/v1/users",
        json={
            "username": "revoked",
            "password": "synthetic-password-2026",
            "role": "viewer",
        },
    ).json()
    login_as(client, "revoked")
    cookie = client.cookies.get("sii_mb_session")
    login_as(client, "admin", "synthetic-test-pass-2026")
    assert (
        client.patch(
            f"/api/v1/users/{created['id']}",
            json={"active": False, "role": "viewer", "scopes": {}},
        ).status_code
        == 200
    )
    client.cookies.clear()
    client.cookies.set("sii_mb_session", cookie)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_upgrade_v01_preserves_indicator(tmp_path, monkeypatch):
    from pathlib import Path

    import sqlalchemy as sa
    from alembic.config import Config

    from alembic import command
    from app.db import make_engine
    from app.migrations import upgrade

    url = f"sqlite+pysqlite:///{tmp_path / 'v01.db'}"
    engine = make_engine(url)
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "alembic"))
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, "0001")
        connection.execute(
            sa.text(
                "INSERT INTO indicators (id,code,name,definition,unit,status,created_at,updated_at) VALUES ('original','IND-ORIGINAL','Original','Original identity preserved','u','draft','2026','2026')"
            )
        )
        connection.execute(sa.text("DROP TABLE alembic_version"))
    upgrade(engine)
    with engine.connect() as connection:
        row = connection.execute(sa.text("SELECT id,active,dimensions_json FROM indicators")).one()
        assert row == ("original", 1, "[]")
    engine.dispose()
