import time
from collections import defaultdict, deque
from scapy.layers.inet import IP, TCP, ICMP


class TrafficAnalyzer:
    def __init__(self, config: dict, alert_manager):
        self.config = config
        self.rules = config["rules"]
        self.alert_manager = alert_manager

        self.port_scan_history = defaultdict(lambda: deque())
        self.icmp_history = defaultdict(lambda: deque())
        self.syn_history = defaultdict(lambda: deque())
        self.ssh_history = defaultdict(lambda: deque())

    def analyze_packet(self, packet):
        if not packet.haslayer(IP):
            return

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        if packet.haslayer(TCP):
            self._analyze_tcp(packet, source_ip, destination_ip)

        if packet.haslayer(ICMP):
            self._analyze_icmp(source_ip)

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
        self._detect_repeated_ssh(source_ip, destination_port)
        self._detect_suspicious_port(source_ip, destination_port)

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

    def _detect_repeated_ssh(self, source_ip: str, destination_port: int):
        rule = self.rules["repeated_ssh"]

        if not rule["enabled"]:
            return

        ssh_port = rule["ssh_port"]

        if destination_port != ssh_port:
            return

        time_window = rule["time_window_seconds"]
        threshold = rule["attempt_threshold"]

        history = self.ssh_history[source_ip]
        history.append((time.time(), destination_port))
        self._cleanup_old_events(history, time_window)

        if len(history) >= threshold:
            self.alert_manager.generate_alert(
                level="ALTO",
                alert_type="INTENTOS_REPETIDOS_SSH",
                source_ip=source_ip,
                description=f"{len(history)} intentos hacia puerto SSH {ssh_port} en {time_window} segundos"
            )
            history.clear()

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
