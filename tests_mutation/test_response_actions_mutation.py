import response_actions
from alert_manager import AlertManager
from response_actions import ActiveResponse


def test_active_response_adds_recommended_block_to_alert(tmp_path):
    manager = AlertManager(
        str(tmp_path / "alerts.json"),
        active_response=ActiveResponse(
            {
                "enabled": True,
                "auto_block_enabled": False,
                "block_minutes": 5,
                "block_alert_types": ["ICMP_FLOOD"],
            }
        ),
    )

    saved = manager.generate_alert(
        "MEDIO",
        "ICMP_FLOOD",
        "192.168.1.50",
        "20 paquetes ICMP en 5 segundos",
    )

    alerts = manager.storage.read()

    assert saved is True
    assert alerts[0]["response_action"]["action"] == "BLOQUEO_TEMPORAL_IP"
    assert alerts[0]["response_action"]["status"] == "RECOMENDADO"
    assert alerts[0]["response_action"]["duration_minutes"] == 5
    assert "192.168.1.50" in alerts[0]["response_action"]["windows_block_command"]


def test_manual_blocks_use_independent_rule_names(monkeypatch):
    monkeypatch.setattr(response_actions.platform, "system", lambda: "Windows")
    monkeypatch.setattr(response_actions.subprocess, "run", lambda *args, **kwargs: None)
    popen_commands = []
    monkeypatch.setattr(
        response_actions.subprocess,
        "Popen",
        lambda command, **kwargs: popen_commands.append(command),
    )

    response = ActiveResponse({"block_minutes": 10})
    first = response.block_ip_temporarily("192.168.1.12")
    second = response.block_ip_temporarily("192.168.1.12")

    assert first["status"] == "BLOQUEO_APLICADO"
    assert second["status"] == "BLOQUEO_APLICADO"
    assert first["windows_rule_name"] != second["windows_rule_name"]
    assert first["windows_rule_name"] in popen_commands[0][-1]
    assert second["windows_rule_name"] in popen_commands[1][-1]
