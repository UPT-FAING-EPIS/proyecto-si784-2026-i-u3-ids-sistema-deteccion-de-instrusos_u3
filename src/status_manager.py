from datetime import datetime
import json
from pathlib import Path


class StatusManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = {}

    def start(self, interface: str, network_info=None):
        self.state = {
            "ids_active": True,
            "started_at": self._now(),
            "last_heartbeat": self._now(),
            "interface": interface or "Scapy default",
            "local_ip": getattr(network_info, "ip_address", "-"),
            "gateway": getattr(network_info, "gateway", "-"),
            "network": getattr(network_info, "network", "-"),
        }
        self._write()

    def heartbeat(self):
        if not self.state:
            self.state = {"ids_active": True}

        self.state["ids_active"] = True
        self.state["last_heartbeat"] = self._now()
        self._write()

    def stop(self):
        if not self.state:
            self.state = {}

        self.state["ids_active"] = False
        self.state["stopped_at"] = self._now()
        self.state["last_heartbeat"] = self._now()
        self._write()

    def _write(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            self._to_json(),
            encoding="utf-8"
        )

    def _to_json(self) -> str:
        return json.dumps(self.state, indent=4, ensure_ascii=False)

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_status(file_path: str) -> dict:
    path = Path(file_path)

    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
