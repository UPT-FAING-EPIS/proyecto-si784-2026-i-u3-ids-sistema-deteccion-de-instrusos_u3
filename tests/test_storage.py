from src.storage import AlertStorage


def test_storage_save_and_read(tmp_path):
    file_path = tmp_path / "alerts.json"
    storage = AlertStorage(str(file_path))

    alert = {
        "timestamp": "2026-01-01 10:00:00",
        "level": "ALTO",
        "type": "PRUEBA",
        "source_ip": "127.0.0.1",
        "description": "Alerta de prueba"
    }

    storage.save(alert)
    data = storage.read()

    assert len(data) == 1
    assert data[0]["type"] == "PRUEBA"
