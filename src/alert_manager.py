from datetime import datetime
import time

try:
    from storage import AlertStorage
except ImportError:
    from src.storage import AlertStorage


class AlertManager:
    def __init__(self, log_file: str, cooldown_seconds: int = 0, active_response=None):
        self.storage = AlertStorage(log_file)
        self.cooldown_seconds = max(0, int(cooldown_seconds or 0))
        self.last_alert_times = {}
        self.active_response = active_response

    def _is_in_cooldown(self, alert_type: str, source_ip: str) -> bool:
        if self.cooldown_seconds == 0:
            return False

        current_time = time.time()
        alert_key = (alert_type, source_ip)
        last_alert_time = self.last_alert_times.get(alert_key)

        if last_alert_time and current_time - last_alert_time < self.cooldown_seconds:
            return True

        self.last_alert_times[alert_key] = current_time
        return False

    def generate_alert(self, level: str, alert_type: str, source_ip: str, description: str):
        if self._is_in_cooldown(alert_type, source_ip):
            return False

        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "type": alert_type,
            "source_ip": source_ip,
            "description": description
        }

        if self.active_response:
            try:
                response = self.active_response.build_response(alert_type, source_ip)
            except ValueError as error:
                response = {
                    "action": "BLOQUEO_TEMPORAL_IP",
                    "status": "NO_APLICADO",
                    "error": str(error),
                }

            if response:
                alert["response_action"] = response

        print(
            f"[ALERTA] RIESGO={level} | "
            f"TIPO={alert_type} | "
            f"ORIGEN={source_ip} | "
            f"DETALLE={description}"
        )

        self.storage.save(alert)
        return True
