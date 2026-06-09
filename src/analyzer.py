import ipaddress
import time
from collections import defaultdict, deque
from datetime import datetime
from scapy.layers.inet import IP, TCP, ICMP

from src.storage import AlertStorage


class TrafficAnalyzer:
    def __init__(self, config: dict, alert_manager, network_info=None):
        self.config = config
        self.rules = config["rules"]
        self.alert_manager = alert_manager
        self.network_info = network_info
        self.local_network = self._build_local_network(network_info)

        traffic_config = config.get("traffic_monitor", {})
        self.traffic_enabled = traffic_config.get("enabled", True)
        self.traffic_storage = AlertStorage(
            traffic_config.get("log_file", "logs/traffic.json"),
            max_records=traffic_config.get("max_records", 100)
        )

        self.port_scan_history = defaultdict(lambda: deque())
        self.icmp_history = defaultdict(lambda: deque())
        self.syn_history = defaultdict(lambda: deque())
        self.brute_force_history = defaultdict(lambda: deque())
        self.connection_frequency_history = defaultdict(lambda: deque())

    def analyze_packet(self, packet):
        if not packet.haslayer(IP):
            return

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst
        self._record_traffic(packet, source_ip, destination_ip)

        if packet.haslayer(TCP):
            self._analyze_tcp(packet, source_ip, destination_ip)

        if packet.haslayer(ICMP):
            self._analyze_icmp(source_ip)

    def _build_local_network(self, network_info):
        if not network_info:
            return None

        try:
            return ipaddress.ip_network(network_info.network, strict=False)
        except ValueError:
            return None

    def _is_local_ip(self, ip_address: str) -> bool:
        if not self.local_network:
            return False

        try:
            return ipaddress.ip_address(ip_address) in self.local_network
        except ValueError:
            return False

    def _classify_traffic(self, source_ip: str, destination_ip: str) -> str:
        if not self.network_info:
            return "DESCONOCIDO"

        local_ip = self.network_info.ip_address
        gateway = self.network_info.gateway
        source_is_local = self._is_local_ip(source_ip)
        destination_is_local = self._is_local_ip(destination_ip)

        if source_ip == gateway or destination_ip == gateway:
            return "GATEWAY"

        if destination_ip == local_ip and not source_is_local:
            return "ENTRANTE"

        if source_ip == local_ip and not destination_is_local:
            return "SALIENTE"

        if source_is_local and destination_is_local:
            return "LOCAL"

        return "EXTERNO"

    def _get_packet_protocol(self, packet) -> str:
        if packet.haslayer(TCP):
            return "TCP"

        if packet.haslayer(ICMP):
            return "ICMP"

        return "IP"

    def _record_traffic(self, packet, source_ip: str, destination_ip: str):
        if not self.traffic_enabled:
            return

        source_port = None
        destination_port = None
        flags = ""

        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            source_port = int(tcp_layer.sport)
            destination_port = int(tcp_layer.dport)
            flags = str(tcp_layer.flags)

        traffic_event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "direction": self._classify_traffic(source_ip, destination_ip),
            "protocol": self._get_packet_protocol(packet),
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "source_port": source_port,
            "destination_port": destination_port,
            "flags": flags
        }

        self.traffic_storage.save(traffic_event)

    def _analyze_tcp(self, packet, source_ip: str, destination_ip: str):
        tcp_layer = packet[TCP]
        destination_port = int(tcp_layer.dport)
        flags = str(tcp_layer.flags)

        print(
            f"[TCP] {source_ip} -> {destination_ip}:{destination_port} "
            f"FLAGS={flags}"
        )

        self._detect_port_scan(source_ip, destination_port)
        self._detect_syn_flood(source_ip, flags)
        self._detect_brute_force(source_ip, destination_port)
        self._detect_connection_frequency(source_ip)
        self._detect_suspicious_port(source_ip, destination_port)
        self._detect_rare_port(source_ip, destination_port)

    def _analyze_icmp(self, source_ip: str):
        print(f"[ICMP] Paquete ICMP detectado desde {source_ip}")
        self._detect_icmp_flood(source_ip)

    def _cleanup_old_events(self, history: deque, time_window: int):
        current_time = time.time()

        while history and current_time - history[0][0] > time_window:
            history.popleft()

    def _detect_port_scan(self, source_ip: str, destination_port: int):
        rule = self.rules["port_scan"]

        if not rule["enabled"]:
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["unique_ports_threshold"]

        history = self.port_scan_history[source_ip]
        history.append((time.time(), destination_port))
        self._cleanup_old_events(history, time_window)

        unique_ports = {port for _, port in history}

        if len(unique_ports) >= threshold:
            self.alert_manager.generate_alert(
                level="ALTO",
                alert_type="ESCANEO_DE_PUERTOS",
                source_ip=source_ip,
                description=f"Acceso a {len(unique_ports)} puertos diferentes en {time_window} segundos"
            )
            history.clear()

    def _detect_icmp_flood(self, source_ip: str):
        rule = self.rules["icmp_flood"]

        if not rule["enabled"]:
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["packet_threshold"]

        history = self.icmp_history[source_ip]
        history.append((time.time(), "ICMP"))
        self._cleanup_old_events(history, time_window)

        if len(history) >= threshold:
            self.alert_manager.generate_alert(
                level="MEDIO",
                alert_type="ICMP_FLOOD",
                source_ip=source_ip,
                description=f"{len(history)} paquetes ICMP en {time_window} segundos"
            )
            history.clear()

    def _detect_syn_flood(self, source_ip: str, flags: str):
        rule = self.rules["syn_flood"]

        if not rule["enabled"]:
            return

        if flags != "S":
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["packet_threshold"]

        history = self.syn_history[source_ip]
        history.append((time.time(), "SYN"))
        self._cleanup_old_events(history, time_window)

        if len(history) >= threshold:
            self.alert_manager.generate_alert(
                level="ALTO",
                alert_type="SYN_FLOOD",
                source_ip=source_ip,
                description=f"{len(history)} paquetes SYN en {time_window} segundos"
            )
            history.clear()

    def _detect_brute_force(self, source_ip: str, destination_port: int):
        rule = self.rules.get("brute_force", {})

        if not rule.get("enabled", False):
            return

        protected_ports = rule.get("ports", {})
        service_name = None

        for name, port in protected_ports.items():
            if destination_port == int(port):
                service_name = name
                break

        if not service_name:
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["attempt_threshold"]
        history_key = (source_ip, service_name)

        history = self.brute_force_history[history_key]
        history.append((time.time(), destination_port))
        self._cleanup_old_events(history, time_window)

        if len(history) >= threshold:
            self.alert_manager.generate_alert(
                level="ALTO",
                alert_type=f"FUERZA_BRUTA_{service_name}",
                source_ip=source_ip,
                description=(
                    f"{len(history)} intentos hacia {service_name} "
                    f"puerto {destination_port} en {time_window} segundos"
                )
            )
            history.clear()

    def _detect_connection_frequency(self, source_ip: str):
        rule = self.rules.get("connection_frequency", {})

        if not rule.get("enabled", False):
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["packet_threshold"]

        history = self.connection_frequency_history[source_ip]
        history.append((time.time(), "TCP"))
        self._cleanup_old_events(history, time_window)

        if len(history) >= threshold:
            self.alert_manager.generate_alert(
                level="MEDIO",
                alert_type="ALTA_FRECUENCIA_CONEXIONES",
                source_ip=source_ip,
                description=f"{len(history)} conexiones TCP en {time_window} segundos"
            )
            history.clear()

    def _detect_rare_port(self, source_ip: str, destination_port: int):
        rule = self.rules.get("rare_ports", {})

        if not rule.get("enabled", False):
            return

        rare_ports = set(rule.get("ports", []))

        if destination_port in rare_ports:
            self.alert_manager.generate_alert(
                level="MEDIO",
                alert_type="PUERTO_RARO",
                source_ip=source_ip,
                description=f"Conexion detectada hacia puerto raro {destination_port}"
            )

    def _detect_suspicious_port(self, source_ip: str, destination_port: int):
        rule = self.rules["suspicious_ports"]

        if not rule["enabled"]:
            return

        suspicious_ports = set(rule["ports"])

        if destination_port in suspicious_ports:
            self.alert_manager.generate_alert(
                level="BAJO",
                alert_type="PUERTO_SOSPECHOSO",
                source_ip=source_ip,
                description=f"Conexión detectada hacia puerto sensible {destination_port}"
            )
