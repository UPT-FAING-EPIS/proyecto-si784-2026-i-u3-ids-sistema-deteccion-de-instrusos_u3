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
