from storage import AlertStorage


def test_storage_save_read_and_max_records(tmp_path):
    storage = AlertStorage(str(tmp_path / "alerts.json"), max_records=2)

    storage.save({"type": "PRIMERA", "source_ip": "127.0.0.1"})
    storage.save({"type": "SEGUNDA", "source_ip": "127.0.0.2"})
    storage.save({"type": "TERCERA", "source_ip": "127.0.0.3"})

    data = storage.read()

    assert len(data) == 2
    assert data[0]["type"] == "SEGUNDA"
    assert data[1]["type"] == "TERCERA"


def test_storage_initializes_clears_and_tolerates_corruption(tmp_path):
    file_path = tmp_path / "nested" / "alerts.json"
    storage = AlertStorage(str(file_path))

    assert file_path.exists()
    assert storage.read() == []

    storage.save({"type": "PRUEBA", "source_ip": "127.0.0.1"})
    assert storage.read()[0]["source_ip"] == "127.0.0.1"

    storage.clear()
    assert storage.read() == []

    file_path.write_text("{json roto", encoding="utf-8")
    assert storage.read() == []
