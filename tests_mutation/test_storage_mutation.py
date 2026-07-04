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
