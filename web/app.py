from collections import Counter
import csv
from datetime import datetime
import io
import json
from pathlib import Path
from flask import Flask, Response, jsonify, render_template

from src.status_manager import read_status
from src.storage import AlertStorage

app = Flask(__name__)

LOG_FILE = Path("logs/alerts.json")
TRAFFIC_LOG_FILE = Path("logs/traffic.json")
STATUS_FILE = Path("logs/status.json")
storage = AlertStorage(str(LOG_FILE))
traffic_storage = AlertStorage(str(TRAFFIC_LOG_FILE), max_records=20)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/alerts")
def api_alerts():
    return jsonify(storage.read())


@app.route("/api/traffic")
def api_traffic():
    return jsonify(traffic_storage.read())


@app.route("/api/status")
def api_status():
    status = read_status(str(STATUS_FILE))
    alerts = storage.read()
    traffic_events = traffic_storage.read()
    heartbeat_age = _heartbeat_age_seconds(status.get("last_heartbeat"))
    heartbeat_is_recent = heartbeat_age is not None and heartbeat_age <= 10

    status["ids_active"] = bool(status.get("ids_active")) and heartbeat_is_recent
    status["heartbeat_age_seconds"] = heartbeat_age
    status["last_alert"] = alerts[-1] if alerts else None
    status["last_traffic"] = traffic_events[-1] if traffic_events else None

    return jsonify(status)


@app.route("/api/charts")
def api_charts():
    alerts = storage.read()

    by_type = Counter(alert.get("type", "DESCONOCIDO") for alert in alerts)
    by_level = Counter(alert.get("level", "DESCONOCIDO") for alert in alerts)
    by_ip = Counter(alert.get("source_ip", "DESCONOCIDO") for alert in alerts)
    by_minute = Counter(
        _timestamp_minute(alert.get("timestamp", ""))
        for alert in alerts
    )
    by_minute.pop("", None)

    return jsonify({
        "alerts_by_type": dict(by_type.most_common()),
        "alerts_by_level": dict(by_level.most_common()),
        "alerts_by_minute": dict(sorted(by_minute.items())),
        "top_ips": dict(by_ip.most_common(5))
    })


@app.route("/api/export/alerts.json")
def export_alerts_json():
    alerts = storage.read()
    content = json.dumps(alerts, indent=4, ensure_ascii=False)

    return Response(
        content,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=alerts.json"}
    )


@app.route("/api/export/alerts.csv")
def export_alerts_csv():
    alerts = storage.read()
    output = io.StringIO()
    fieldnames = ["timestamp", "level", "type", "source_ip", "description"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    writer.writerows(alerts)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=alerts.csv"}
    )


@app.route("/api/export/traffic.json")
def export_traffic_json():
    traffic_events = traffic_storage.read()
    content = json.dumps(traffic_events, indent=4, ensure_ascii=False)

    return Response(
        content,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=traffic.json"}
    )


@app.route("/api/export/traffic.csv")
def export_traffic_csv():
    traffic_events = traffic_storage.read()
    output = io.StringIO()
    fieldnames = [
        "timestamp",
        "direction",
        "protocol",
        "source_ip",
        "destination_ip",
        "source_port",
        "destination_port",
        "flags"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()
    writer.writerows(traffic_events)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=traffic.csv"}
    )


@app.route("/api/stats")
def api_stats():
    alerts = storage.read()

    total_alerts = len(alerts)
    by_type = Counter(alert.get("type", "DESCONOCIDO") for alert in alerts)
    by_level = Counter(alert.get("level", "DESCONOCIDO") for alert in alerts)
    by_ip = Counter(alert.get("source_ip", "DESCONOCIDO") for alert in alerts)

    return jsonify({
        "total_alerts": total_alerts,
        "by_type": dict(by_type),
        "by_level": dict(by_level),
        "top_ips": dict(by_ip.most_common(5))
    })


def _heartbeat_age_seconds(last_heartbeat):
    if not last_heartbeat:
        return None

    try:
        heartbeat_time = datetime.strptime(last_heartbeat, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return int((datetime.now() - heartbeat_time).total_seconds())


def _timestamp_minute(timestamp: str) -> str:
    if not timestamp:
        return ""

    return timestamp[:16]


@app.route("/api/clear", methods=["POST"])
def api_clear():
    storage.clear()
    return jsonify({"status": "ok", "message": "Alertas eliminadas"})
