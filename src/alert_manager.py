from datetime import datetime
from src.storage import AlertStorage


class AlertManager:
    def __init__(self, log_file: str):
        self.storage = AlertStorage(log_file)

    def generate_alert(self, level: str, alert_type: str, source_ip: str, description: str):
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "type": alert_type,
            "source_ip": source_ip,
            "description": description
        }

        print(
            f"[ALERTA] RIESGO={level} | "
            f"TIPO={alert_type} | "
            f"ORIGEN={source_ip} | "
            f"DETALLE={description}"
        )

        self.storage.save(alert)
