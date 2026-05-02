from collections import Counter
from pathlib import Path
from flask import Flask, jsonify, render_template

from src.storage import AlertStorage

app = Flask(__name__)

LOG_FILE = Path("logs/alerts.json")
storage = AlertStorage(str(LOG_FILE))


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/alerts")
def api_alerts():
    return jsonify(storage.read())


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


@app.route("/api/clear", methods=["POST"])
def api_clear():
    storage.clear()
    return jsonify({"status": "ok", "message": "Alertas eliminadas"})
