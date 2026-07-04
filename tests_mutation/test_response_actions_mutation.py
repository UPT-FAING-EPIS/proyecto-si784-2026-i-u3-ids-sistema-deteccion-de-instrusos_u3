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


def test_active_response_disabled_and_invalid_ip_are_handled():
    disabled = ActiveResponse({"enabled": False})
    assert disabled.build_response("ICMP_FLOOD", "192.168.1.50") is None

    response = ActiveResponse({"block_alert_types": ["ICMP_FLOOD"], "block_minutes": 0})
    assert response.block_minutes == 1
    assert response.build_response("PUERTO_RARO", "192.168.1.50") is None

    try:
        response.build_response("ICMP_FLOOD", "not-an-ip")
    except ValueError as error:
        assert "IP origen invalida" in str(error)
    else:
        raise AssertionError("build_response must reject invalid IP addresses")


def test_active_response_builds_sanitized_recommendation(monkeypatch):
    monkeypatch.setattr(response_actions.uuid, "uuid4", lambda: type("Token", (), {"hex": "abcdef1234567890"})())
    response = ActiveResponse(
        {
            "auto_block_enabled": False,
            "block_minutes": 3,
            "block_alert_types": ["ICMP FLOOD!"],
            "windows_firewall_rule_prefix": "IDS Rule",
        }
    )

    action = response.build_response("ICMP FLOOD!", " 192.168.1.77 ")

    assert action["status"] == "RECOMENDADO"
    assert action["source_ip"] == "192.168.1.77"
    assert action["duration_minutes"] == 3
    assert action["windows_rule_name"] == "IDS Rule ICMP_FLOOD_ 192.168.1.77 abcdef123456"
    assert 'DisplayName "IDS Rule ICMP_FLOOD_ 192.168.1.77 abcdef123456"' in action["windows_block_command"]


def test_non_windows_manual_block_does_not_execute_firewall(monkeypatch):
    monkeypatch.setattr(response_actions.platform, "system", lambda: "Linux")
    response = ActiveResponse({"block_minutes": 4})

    result = response.block_ip_temporarily("192.168.1.90")

    assert result["status"] == "NO_APLICADO"
    assert "Windows Firewall" in result["error"]
