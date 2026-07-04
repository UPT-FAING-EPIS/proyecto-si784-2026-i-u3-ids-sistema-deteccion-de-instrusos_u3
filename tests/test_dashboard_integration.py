import pytest

from src.storage import AlertStorage
from web import app as dashboard_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        dashboard_app,
        "storage",
        AlertStorage(str(tmp_path / "alerts.json")),
    )
    monkeypatch.setattr(
        dashboard_app,
        "traffic_storage",
        AlertStorage(str(tmp_path / "traffic.json"), max_records=20),
    )
    monkeypatch.setattr(
        dashboard_app,
        "policy_storage",
        AlertStorage(str(tmp_path / "policies.json")),
    )
    monkeypatch.setattr(dashboard_app, "STATUS_FILE", tmp_path / "status.json")

    return dashboard_app.app.test_client()


@pytest.mark.integration
def test_dashboard_and_core_apis_are_available(client):
    routes = [
        "/",
        "/attack-lab",
        "/api/status",
        "/api/alerts",
        "/api/traffic",
        "/api/incidents",
        "/api/charts",
        "/api/stats",
        "/api/suricata/status",
        "/api/suricata/alerts",
        "/api/ips/policies",
    ]

    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, route


@pytest.mark.integration
def test_simulation_registers_alert_and_traffic_without_real_network(client):
    response = client.post("/api/simulate/brute_force")

    assert response.status_code == 200
    assert response.get_json()["alert"]["type"] == "FUERZA_BRUTA_SSH"

    alerts = client.get("/api/alerts").get_json()
    traffic = client.get("/api/traffic").get_json()

    assert alerts[-1]["type"] == "FUERZA_BRUTA_SSH"
    assert traffic[-1]["destination_port"] == 22


@pytest.mark.integration
def test_invalid_ips_routes_return_controlled_errors(client):
    firewall_response = client.post("/api/firewall/block-ssh-ip", json={"ip": "no-ip"})
    youtube_response = client.post("/api/ips/youtube-block-command", json={"ip": "no-ip"})

    assert firewall_response.status_code == 400
    assert youtube_response.status_code == 400
