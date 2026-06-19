from collections import Counter
import csv
from datetime import datetime
import io
import ipaddress
import json
from pathlib import Path
import subprocess
import sys
from flask import Flask, Response, jsonify, render_template, request

from src.network_scanner import scan_local_network
from src.real_scan import run_local_nmap_scan
from src.response_actions import ActiveResponse
from src.status_manager import read_status
from src.storage import AlertStorage
from src.suricata_integration import (
    DEFAULT_EVE_LOG_FILE,
    DEFAULT_LOCAL_RULES_FILE,
    append_demo_suricata_alert,
    build_firewall_block_command,
    build_inline_ips_plan,
    build_youtube_block_for_ip,
    build_youtube_policy_commands,
    get_suricata_status,
    read_suricata_alerts,
)

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
app = Flask(__name__, template_folder=str(BASE_DIR / "web" / "templates"))

LOG_FILE = Path("logs/alerts.json")
TRAFFIC_LOG_FILE = Path("logs/traffic.json")
STATUS_FILE = Path("logs/status.json")
POLICY_FILE = Path("logs/policies.json")
CONFIG_FILE = Path("config.json")
storage = AlertStorage(str(LOG_FILE))
traffic_storage = AlertStorage(str(TRAFFIC_LOG_FILE), max_records=20)
policy_storage = AlertStorage(str(POLICY_FILE))

SCAN_RISK_ORDER = {"BAJO": 1, "MEDIO": 2, "ALTO": 3}
SCAN_SENSITIVE_PORTS = {21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5900}
SCAN_RARE_PORTS = {1337, 2323, 31337, 5555, 6667, 9001}

SIMULATED_ALERTS = {
    "port_scan": {
        "level": "ALTO",
        "type": "ESCANEO_DE_PUERTOS",
        "source_ip": "10.10.10.25",
        "description": "SIMULACION: acceso rapido a multiples puertos del gateway.",
        "traffic": {
            "direction": "LOCAL",
            "protocol": "TCP",
            "source_ip": "10.10.10.25",
            "destination_ip": "192.168.1.1",
            "source_port": 50421,
            "destination_port": 80,
            "flags": "S"
        }
    },
    "brute_force": {
        "level": "ALTO",
        "type": "FUERZA_BRUTA_SSH",
        "source_ip": "10.10.10.44",
        "description": "SIMULACION: varios intentos repetidos hacia SSH en pocos segundos.",
        "traffic": {
            "direction": "LOCAL",
            "protocol": "TCP",
            "source_ip": "10.10.10.44",
            "destination_ip": "192.168.1.33",
            "source_port": 51222,
            "destination_port": 22,
            "flags": "S"
        }
    },
    "syn_flood": {
        "level": "ALTO",
        "type": "SYN_FLOOD",
        "source_ip": "10.10.10.77",
        "description": "SIMULACION: exceso de paquetes SYN desde una misma IP.",
        "traffic": {
            "direction": "ENTRANTE",
            "protocol": "TCP",
            "source_ip": "10.10.10.77",
            "destination_ip": "192.168.1.33",
            "source_port": 53000,
            "destination_port": 443,
            "flags": "S"
        }
    },
    "icmp_flood": {
        "level": "MEDIO",
        "type": "ICMP_FLOOD",
        "source_ip": "10.10.10.88",
        "description": "SIMULACION: trafico ICMP repetitivo detectado.",
        "traffic": {
            "direction": "LOCAL",
            "protocol": "ICMP",
            "source_ip": "10.10.10.88",
            "destination_ip": "192.168.1.33",
            "source_port": None,
            "destination_port": None,
            "flags": ""
        }
    },
    "rare_port": {
        "level": "MEDIO",
        "type": "PUERTO_RARO",
        "source_ip": "10.10.10.99",
        "description": "SIMULACION: conexion hacia puerto raro 31337.",
        "traffic": {
            "direction": "LOCAL",
            "protocol": "TCP",
            "source_ip": "10.10.10.99",
            "destination_ip": "192.168.1.33",
            "source_port": 54000,
            "destination_port": 31337,
            "flags": "S"
        }
    },
    "connection_frequency": {
        "level": "MEDIO",
        "type": "ALTA_FRECUENCIA_CONEXIONES",
        "source_ip": "10.10.10.66",
        "description": "SIMULACION: muchas conexiones TCP desde la misma IP.",
        "traffic": {
            "direction": "LOCAL",
            "protocol": "TCP",
            "source_ip": "10.10.10.66",
            "destination_ip": "192.168.1.33",
            "source_port": 55000,
            "destination_port": 80,
            "flags": "S"
        }
    }
}

REMOTE_TRAFFIC_ALERTS = {
    "brute_force": {
        "level": "ALTO",
        "type": "TRAFICO_REAL_LAB_FUERZA_BRUTA_SSH",
        "description": "Trafico HTTP real de laboratorio equivalente a intentos repetidos SSH."
    },
    "syn_flood": {
        "level": "ALTO",
        "type": "TRAFICO_REAL_LAB_SYN_FLOOD",
        "description": "Trafico HTTP real controlado para validar deteccion de rafaga tipo SYN sin saturar la red."
    },
    "icmp_flood": {
        "level": "MEDIO",
        "type": "TRAFICO_REAL_LAB_ICMP_FLOOD",
        "description": "Trafico HTTP real de laboratorio equivalente a rafaga ICMP controlada."
    },
    "rare_port": {
        "level": "MEDIO",
        "type": "TRAFICO_REAL_LAB_PUERTO_RARO",
        "description": "Trafico HTTP real de laboratorio equivalente a acceso a puerto raro."
    },
    "connection_frequency": {
        "level": "MEDIO",
        "type": "TRAFICO_REAL_LAB_ALTA_FRECUENCIA",
        "description": "Muchas solicitudes HTTP reales desde la misma IP remota."
    },
}


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/attack-lab")
def attack_lab():
    return render_template("attack_lab.html")


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
    fieldnames = [
        "timestamp",
        "level",
        "category",
        "type",
        "source_ip",
        "target_ip",
        "target_port",
        "evidence_count",
        "response_status",
        "response_action",
        "response_command",
        "description",
    ]
    for alert in alerts:
        response_action = alert.get("response_action") or {}
        alert["response_status"] = response_action.get("status", "")
        alert["response_action"] = response_action.get("action", "")
        alert["response_command"] = response_action.get("windows_block_command", "")

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


@app.route("/api/network/devices")
def api_network_devices():
    try:
        return jsonify(scan_local_network())
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error),
            "devices": []
        }), 500


@app.route("/api/real-scan/nmap", methods=["POST"])
def api_real_nmap_scan():
    data = request.get_json(silent=True) or {}

    try:
        result = run_local_nmap_scan(
            target=data.get("target", ""),
            ports=data.get("ports", "")
        )
    except (RuntimeError, ValueError, subprocess.SubprocessError) as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    requester_ip = _request_source_ip()
    scan_risk = _classify_nmap_scan_risk(
        requester_ip=requester_ip,
        target_ip=result["target"],
        ports=result["ports"],
    )
    storage.save({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": scan_risk["level"],
        "category": "ESCANEO_REAL",
        "type": "ESCANEO_REAL_NMAP",
        "source_ip": requester_ip,
        "target_ip": result["target"],
        "target_port": result["ports"],
        "evidence_count": scan_risk["evidence_count"],
        "description": (
            f"Escaneo real solicitado desde {requester_ip} "
            f"contra {result['target']} "
            f"en puertos {result['ports']}. "
            f"Riesgo {scan_risk['level']}: {scan_risk['reason']}."
        )
    })

    return jsonify({
        "status": "ok",
        "message": "Escaneo Nmap completado",
        "result": result
    })


@app.route("/api/suricata/status")
def api_suricata_status():
    config = _suricata_config()

    return jsonify(get_suricata_status(
        config["eve_log_file"],
        config["local_rules_file"]
    ))


@app.route("/api/suricata/alerts")
def api_suricata_alerts():
    config = _suricata_config()

    return jsonify(read_suricata_alerts(
        config["eve_log_file"],
        max_events=config["max_alerts"]
    ))


@app.route("/api/suricata/demo-alert", methods=["POST"])
def api_suricata_demo_alert():
    config = _suricata_config()
    alert = append_demo_suricata_alert(config["eve_log_file"])

    return jsonify({
        "status": "ok",
        "message": "Alerta demo Suricata IPS generada",
        "alert": alert
    })


@app.route("/api/ips/block-command", methods=["POST"])
def api_ips_block_command():
    data = request.get_json(silent=True) or {}

    try:
        command = build_firewall_block_command(data.get("ip"))
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    return jsonify({"status": "ok", "command": command})


@app.route("/api/ips/youtube-policy")
def api_ips_youtube_policy():
    return jsonify(build_youtube_policy_commands())


@app.route("/api/ips/youtube-block-command", methods=["POST"])
def api_ips_youtube_block_command():
    data = request.get_json(silent=True) or {}

    try:
        policy = build_youtube_block_for_ip(data.get("ip"))
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    return jsonify({"status": "ok", "policy": policy})


@app.route("/api/ips/policies")
def api_ips_policies():
    return jsonify(policy_storage.read())


@app.route("/api/ips/youtube-policy/save", methods=["POST"])
def api_ips_save_youtube_policy():
    data = request.get_json(silent=True) or {}

    try:
        policy = build_youtube_block_for_ip(data.get("ip"))
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "BLOQUEO_YOUTUBE",
        "target_ip": policy["ip"],
        "domains": policy["domains"],
        "status": "GENERADA_PENDIENTE_DE_APLICAR",
        "apply_at": "Gateway, router, DNS filtering o Suricata IPS inline",
        "note": policy["note"],
        "suricata_rules": policy["suricata_rules"],
    }
    policy_storage.save(record)
    storage.save({
        "timestamp": record["timestamp"],
        "level": "MEDIO",
        "category": "POLITICA_RESPUESTA",
        "type": "POLITICA_BLOQUEO_YOUTUBE",
        "source_ip": policy["ip"],
        "target_ip": policy["ip"],
        "target_port": "HTTPS/QUIC",
        "evidence_count": len(policy["domains"]),
        "description": (
            f"Politica generada para bloquear YouTube a {policy['ip']}. "
            "Pendiente de aplicar en gateway/router/DNS/IPS inline."
        )
    })

    return jsonify({
        "status": "ok",
        "message": "Politica YouTube guardada",
        "policy": record
    })


@app.route("/api/ips/inline-plan", methods=["POST"])
def api_ips_inline_plan():
    data = request.get_json(silent=True) or {}

    try:
        plan = build_inline_ips_plan(
            interface=data.get("interface", "eth0"),
            queue_num=data.get("queue_num", 0)
        )
    except (TypeError, ValueError) as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    return jsonify({"status": "ok", "plan": plan})


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


def _classify_nmap_scan_risk(requester_ip: str, target_ip: str, ports: str) -> dict:
    scanned_ports = _expand_port_selection(ports)
    recent_repeats = _recent_nmap_scan_count(requester_ip, target_ip)
    reasons = []
    level = "BAJO"

    if len(scanned_ports) >= 100:
        level = _max_scan_level(level, "MEDIO")
        reasons.append(f"escaneo de {len(scanned_ports)} puertos")

    if len(scanned_ports) >= 1000:
        level = _max_scan_level(level, "ALTO")
        reasons.append("rango amplio de 1000 puertos")

    sensitive_hits = sorted(SCAN_SENSITIVE_PORTS.intersection(scanned_ports))
    if sensitive_hits:
        level = _max_scan_level(level, "MEDIO")
        reasons.append("incluye puertos sensibles " + ",".join(str(port) for port in sensitive_hits[:6]))

    rare_hits = sorted(SCAN_RARE_PORTS.intersection(scanned_ports))
    if rare_hits:
        level = _max_scan_level(level, "ALTO")
        reasons.append("incluye puertos raros " + ",".join(str(port) for port in rare_hits))

    if recent_repeats >= 2:
        level = _max_scan_level(level, "ALTO")
        reasons.append(f"{recent_repeats + 1} escaneos recientes desde la misma IP")

    if not reasons:
        reasons.append("escaneo pequeno y no repetido")

    return {
        "level": level,
        "reason": "; ".join(reasons),
        "evidence_count": max(1, len(scanned_ports)),
    }


def _max_scan_level(current: str, candidate: str) -> str:
    return candidate if SCAN_RISK_ORDER[candidate] > SCAN_RISK_ORDER[current] else current


def _expand_port_selection(ports: str) -> set:
    selected_ports = set()

    for part in str(ports or "").split(","):
        clean_part = part.strip()

        if not clean_part:
            continue

        if "-" in clean_part:
            start_text, end_text = clean_part.split("-", 1)
            try:
                start_port = int(start_text)
                end_port = int(end_text)
            except ValueError:
                continue

            selected_ports.update(range(max(1, start_port), min(65535, end_port) + 1))
            continue

        try:
            selected_ports.add(int(clean_part))
        except ValueError:
            continue

    return selected_ports


def _recent_nmap_scan_count(requester_ip: str, target_ip: str, window_minutes: int = 10) -> int:
    now = datetime.now()
    count = 0

    for alert in reversed(storage.read()):
        if alert.get("type") != "ESCANEO_REAL_NMAP":
            continue

        if alert.get("source_ip") != requester_ip or alert.get("target_ip") != target_ip:
            continue

        try:
            alert_time = datetime.strptime(alert.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        age_seconds = (now - alert_time).total_seconds()

        if age_seconds < 0:
            continue

        if age_seconds > window_minutes * 60:
            break

        count += 1

    return count


def _suricata_config() -> dict:
    config = {}

    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            config = {}

    suricata_config = config.get("suricata", {})

    return {
        "enabled": bool(suricata_config.get("enabled", True)),
        "eve_log_file": suricata_config.get("eve_log_file", DEFAULT_EVE_LOG_FILE),
        "local_rules_file": suricata_config.get("local_rules_file", DEFAULT_LOCAL_RULES_FILE),
        "max_alerts": int(suricata_config.get("max_alerts", 100)),
    }


def _active_response_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}

    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    return config.get("active_response", {})


def _has_ssh_brute_force_alert(source_ip: str) -> bool:
    return any(
        alert.get("type") == "FUERZA_BRUTA_SSH"
        and alert.get("source_ip") == source_ip
        for alert in storage.read()
    )


@app.route("/api/clear", methods=["POST"])
def api_clear():
    storage.clear()
    return jsonify({"status": "ok", "message": "Alertas eliminadas"})


@app.route("/api/firewall/block-ssh-ip", methods=["POST"])
def api_firewall_block_ssh_ip():
    data = request.get_json(silent=True) or {}

    try:
        source_ip = str(ipaddress.ip_address(str(data.get("ip", "")).strip()))
    except ValueError:
        return jsonify({"status": "error", "message": "Ingresa una IP valida."}), 400

    if not _has_ssh_brute_force_alert(source_ip):
        return jsonify({
            "status": "error",
            "message": "Solo se puede bloquear una IP que tenga una alerta FUERZA_BRUTA_SSH registrada."
        }), 400

    response = ActiveResponse(_active_response_config()).block_ip_temporarily(
        source_ip,
        alert_type="FUERZA_BRUTA_SSH",
    )

    if response.get("status") != "BLOQUEO_APLICADO":
        return jsonify({
            "status": "error",
            "message": response.get("error", "No se pudo aplicar el bloqueo."),
        }), 500

    storage.save({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": "ALTO",
        "category": "RESPUESTA_ACTIVA",
        "type": "BLOQUEO_TEMPORAL_SSH",
        "source_ip": source_ip,
        "target_ip": "Este equipo",
        "target_port": 22,
        "evidence_count": 1,
        "response_action": response,
        "description": (
            f"Firewall de Windows bloqueo conexiones entrantes desde {source_ip} "
            f"por {response['duration_minutes']} minutos tras alerta de fuerza bruta SSH."
        ),
    })

    return jsonify({
        "status": "ok",
        "message": (
            f"IP {source_ip} bloqueada en este equipo hasta {response['block_until']}."
        ),
        "response_action": response,
    })


@app.route("/api/simulate/<attack_type>", methods=["POST"])
def api_simulate_attack(attack_type):
    simulation = SIMULATED_ALERTS.get(attack_type)

    if not simulation:
        return jsonify({
            "status": "error",
            "message": "Tipo de simulacion no soportado"
        }), 404

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = {
        "timestamp": timestamp,
        "level": simulation["level"],
        "category": "SIMULACION_LOCAL",
        "type": simulation["type"],
        "source_ip": simulation["source_ip"],
        "target_ip": simulation["traffic"].get("destination_ip"),
        "target_port": simulation["traffic"].get("destination_port"),
        "evidence_count": 1,
        "description": simulation["description"]
    }
    traffic_event = {
        "timestamp": timestamp,
        **simulation["traffic"]
    }

    storage.save(alert)
    traffic_storage.save(traffic_event)

    return jsonify({
        "status": "ok",
        "message": f"Simulacion generada: {alert['type']}",
        "alert": alert
    })


@app.route("/api/remote-attack/<attack_type>", methods=["POST"])
def api_remote_attack(attack_type):
    simulation = SIMULATED_ALERTS.get(attack_type)

    if not simulation:
        return jsonify({
            "status": "error",
            "message": "Tipo de ataque remoto no soportado"
        }), 404

    source_ip = _request_source_ip()
    target_ip = simulation["traffic"].get("destination_ip")
    target_port = simulation["traffic"].get("destination_port")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = {
        "timestamp": timestamp,
        "level": simulation["level"],
        "category": "SIMULACION_REMOTA",
        "type": f"REMOTO_{simulation['type']}",
        "source_ip": source_ip,
        "target_ip": target_ip,
        "target_port": target_port,
        "evidence_count": 1,
        "description": (
            f"LAB REMOTO: {simulation['description']} "
            f"Solicitud recibida desde {source_ip}."
        )
    }
    traffic_event = {
        "timestamp": timestamp,
        **simulation["traffic"],
        "source_ip": source_ip,
        "destination_ip": target_ip,
        "destination_port": target_port,
    }

    storage.save(alert)
    traffic_storage.save(traffic_event)

    return jsonify({
        "status": "ok",
        "message": f"Ataque remoto simulado: {alert['type']}",
        "alert": alert
    })


@app.route("/api/remote-lab-traffic/<traffic_type>", methods=["POST"])
def api_remote_lab_traffic(traffic_type):
    template = REMOTE_TRAFFIC_ALERTS.get(traffic_type)

    if not template:
        return jsonify({
            "status": "error",
            "message": "Tipo de trafico remoto no soportado"
        }), 404

    data = request.get_json(silent=True) or {}
    total = _bounded_int(data.get("total"), 1, 100, 1)
    sequence = _bounded_int(data.get("sequence"), 1, total, 1)
    is_final = bool(data.get("final", False))
    source_ip = _request_source_ip()

    if traffic_type == "syn_flood":
        total = min(total, 30)
        sequence = min(sequence, total)

    try:
        target = _validated_target(data.get("target"))
        destination_port = _bounded_int(data.get("destination_port"), 1, 65535, 5000)
        duration_seconds = _bounded_int(data.get("duration_seconds"), 1, 30, 3)
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400

    if traffic_type == "syn_flood":
        duration_seconds = max(duration_seconds, 3)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    traffic_storage.save({
        "timestamp": timestamp,
        "direction": "REMOTO_LAB",
        "protocol": "HTTP",
        "source_ip": source_ip,
        "destination_ip": target,
        "source_port": None,
        "destination_port": destination_port,
        "flags": f"{traffic_type} CONTROLADO {sequence}/{total}"
    })

    alert = None

    if is_final:
        alert = {
            "timestamp": timestamp,
            "level": template["level"],
            "category": "TRAFICO_REAL_LAB_CONTROLADO",
            "type": template["type"],
            "source_ip": source_ip,
            "target_ip": target,
            "target_port": destination_port,
            "evidence_count": total,
            "duration_seconds": duration_seconds,
            "mode": "CONTROLADO",
            "description": (
                f"{template['description']} "
                f"Origen remoto {source_ip}; objetivo declarado {target}; "
                f"puerto declarado {destination_port}; "
                f"solicitudes recibidas {total} en {duration_seconds}s; "
                "modo CONTROLADO con limites de seguridad."
            )
        }
        storage.save(alert)

    return jsonify({
        "status": "ok",
        "message": "Trafico remoto registrado",
        "source_ip": source_ip,
        "sequence": sequence,
        "total": total,
        "target": target,
        "destination_port": destination_port,
        "alert": alert
    })


def _request_source_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For", "")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr or "DESCONOCIDO"


def _bounded_int(value, minimum: int, maximum: int, default: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default

    return max(minimum, min(number, maximum))


def _validated_target(value) -> str:
    target = str(value or "dashboard").strip()

    if not target or target.lower() == "dashboard":
        return "dashboard"

    try:
        return str(ipaddress.ip_address(target))
    except ValueError as error:
        raise ValueError("Ingresa una IP objetivo valida o deja el campo vacio.") from error
