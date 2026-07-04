from alert_manager import AlertManager


def test_alert_manager_cooldown_blocks_repeated_alert(tmp_path):
    manager = AlertManager(str(tmp_path / "alerts.json"), cooldown_seconds=10)

    first_saved = manager.generate_alert(
        "ALTO",
        "ESCANEO_DE_PUERTOS",
        "192.168.1.33",
        "Primera alerta",
    )
    second_saved = manager.generate_alert(
        "ALTO",
        "ESCANEO_DE_PUERTOS",
        "192.168.1.33",
        "Alerta repetida",
    )

    assert first_saved is True
    assert second_saved is False
    assert len(manager.storage.read()) == 1


def test_alert_manager_allows_distinct_alert_keys(tmp_path):
    manager = AlertManager(str(tmp_path / "alerts.json"), cooldown_seconds=10)

    manager.generate_alert("ALTO", "ESCANEO_DE_PUERTOS", "192.168.1.33", "Alerta")
    manager.generate_alert("ALTO", "SYN_FLOOD", "192.168.1.33", "Otro tipo")
    manager.generate_alert("ALTO", "ESCANEO_DE_PUERTOS", "192.168.1.40", "Otra IP")

    assert len(manager.storage.read()) == 3


def test_alert_manager_persists_expected_alert_fields(tmp_path):
    manager = AlertManager(str(tmp_path / "alerts.json"), cooldown_seconds=-5)

    assert manager.cooldown_seconds == 0
    assert manager.generate_alert("MEDIO", "ICMP_FLOOD", "10.0.0.8", "Trafico ICMP alto")
    assert manager.generate_alert("MEDIO", "ICMP_FLOOD", "10.0.0.8", "Sin cooldown")

    alerts = manager.storage.read()
    assert len(alerts) == 2
    assert alerts[0]["level"] == "MEDIO"
    assert alerts[0]["type"] == "ICMP_FLOOD"
    assert alerts[0]["source_ip"] == "10.0.0.8"
    assert alerts[0]["description"] == "Trafico ICMP alto"
    assert "timestamp" in alerts[0]
