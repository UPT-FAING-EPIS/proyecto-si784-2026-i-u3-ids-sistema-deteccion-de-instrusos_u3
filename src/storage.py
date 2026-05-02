import json
from pathlib import Path
from threading import Lock


class AlertStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = Lock()

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def save(self, alert: dict):
        with self.lock:
            data = self.read()
            data.append(alert)
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def read(self) -> list:
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def clear(self):
        with self.lock:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
