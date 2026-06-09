from src.analyzer import TrafficAnalyzer
from src.network_utils import NetworkInfo


class DummyAlertManager:
    def generate_alert(self, level, alert_type, source_ip, description):
        return True


def build_analyzer(tmp_path):
    config = {
        "traffic_monitor": {
            "enabled": True,
            "log_file": str(tmp_path / "traffic.json"),
            "max_records": 100
        },
        "rules": {
            "port_scan": {"enabled": False},
            "icmp_flood": {"enabled": False},
            "syn_flood": {"enabled": False},
            "brute_force": {"enabled": False},
            "suspicious_ports": {"enabled": False}
        }
    }
    network_info = NetworkInfo(
        interface="Ethernet",
        interface_index=8,
        ip_address="192.168.1.33",
        prefix_length=24,
        gateway="192.168.1.1",
        network="192.168.1.0/24"
    )

    return TrafficAnalyzer(config, DummyAlertManager(), network_info=network_info)


def test_classifies_incoming_traffic(tmp_path):
    analyzer = build_analyzer(tmp_path)

    assert analyzer._classify_traffic("45.162.90.157", "192.168.1.33") == "ENTRANTE"


def test_classifies_outgoing_traffic(tmp_path):
    analyzer = build_analyzer(tmp_path)

    assert analyzer._classify_traffic("192.168.1.33", "8.8.8.8") == "SALIENTE"


def test_classifies_local_traffic(tmp_path):
    analyzer = build_analyzer(tmp_path)

    assert analyzer._classify_traffic("192.168.1.50", "192.168.1.33") == "LOCAL"


def test_classifies_gateway_traffic(tmp_path):
    analyzer = build_analyzer(tmp_path)

    assert analyzer._classify_traffic("192.168.1.33", "192.168.1.1") == "GATEWAY"
