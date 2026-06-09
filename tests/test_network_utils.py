from src.network_utils import _network_info_from_adapter


def test_network_info_detects_192_network():
    network_info = _network_info_from_adapter({
        "InterfaceAlias": "Wi-Fi",
        "InterfaceIndex": 10,
        "IPAddress": "192.168.1.33",
        "PrefixLength": 24,
        "Gateway": "192.168.1.1",
    })

    assert network_info.interface == "Wi-Fi"
    assert network_info.ip_address == "192.168.1.33"
    assert network_info.gateway == "192.168.1.1"
    assert network_info.network == "192.168.1.0/24"


def test_network_info_detects_172_network():
    network_info = _network_info_from_adapter({
        "InterfaceAlias": "Ethernet",
        "InterfaceIndex": 4,
        "IPAddress": "172.16.5.20",
        "PrefixLength": 24,
        "Gateway": "172.16.5.1",
    })

    assert network_info.interface == "Ethernet"
    assert network_info.ip_address == "172.16.5.20"
    assert network_info.gateway == "172.16.5.1"
    assert network_info.network == "172.16.5.0/24"


def test_network_info_detects_10_network():
    network_info = _network_info_from_adapter({
        "InterfaceAlias": "Wi-Fi",
        "InterfaceIndex": 6,
        "IPAddress": "10.0.0.15",
        "PrefixLength": 24,
        "Gateway": "10.0.0.1",
    })

    assert network_info.interface == "Wi-Fi"
    assert network_info.ip_address == "10.0.0.15"
    assert network_info.gateway == "10.0.0.1"
    assert network_info.network == "10.0.0.0/24"
