from pathlib import Path
from tempfile import TemporaryDirectory

from behave import given, then, when

from src.storage import AlertStorage
from web import app as dashboard_app


@given("el dashboard Flask esta disponible")
def step_dashboard_available(context):
    context.bdd_tmpdir = TemporaryDirectory()
    base_path = Path(context.bdd_tmpdir.name)
    context.tmp_alerts = AlertStorage(str(base_path / "alerts.json"))
    context.tmp_traffic = AlertStorage(str(base_path / "traffic.json"), max_records=20)
    context.tmp_policies = AlertStorage(str(base_path / "policies.json"))

    dashboard_app.storage = context.tmp_alerts
    dashboard_app.traffic_storage = context.tmp_traffic
    dashboard_app.policy_storage = context.tmp_policies
    dashboard_app.STATUS_FILE = base_path / "status.json"
    context.client = dashboard_app.app.test_client()


@when("consulto la API de estado")
def step_get_status(context):
    context.response = context.client.get("/api/status")


@then("recibo un estado valido del IDS")
def step_status_is_valid(context):
    payload = context.response.get_json()

    assert context.response.status_code == 200
    assert "ids_active" in payload
    assert "last_alert" in payload
    assert "last_traffic" in payload


@when("genero una simulacion de fuerza bruta SSH")
def step_generate_brute_force(context):
    context.response = context.client.post("/api/simulate/brute_force")


@then("la alerta queda registrada en el historial")
def step_alert_is_saved(context):
    payload = context.response.get_json()
    alerts = context.client.get("/api/alerts").get_json()

    assert context.response.status_code == 200
    assert payload["alert"]["type"] == "FUERZA_BRUTA_SSH"
    assert alerts[-1]["type"] == "FUERZA_BRUTA_SSH"
