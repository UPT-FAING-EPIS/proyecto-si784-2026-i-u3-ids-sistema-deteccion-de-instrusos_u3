import threading

from src.packet_capture import PacketCapture
from src.analyzer import TrafficAnalyzer
from src.alert_manager import AlertManager
from src.network_utils import detect_network_info
from src.status_manager import StatusManager
from src.utils import load_config, print_banner


def resolve_network_info(config: dict):
    interface = config.get("interface", "")
    network_config = config.get("network", {})
    should_detect = (
        network_config.get("auto_detect", False)
        or (isinstance(interface, str) and interface.lower() == "auto")
    )

    if not should_detect:
        return None

    try:
        network_info = detect_network_info()
    except Exception as error:
        print(f"[AVISO] No se pudo detectar la red automaticamente: {error}")
        return None

    print(f"[INFO] Interfaz detectada automaticamente: {network_info.interface}")
    print(f"[INFO] IP local detectada: {network_info.ip_address}")
    print(f"[INFO] Gateway detectado: {network_info.gateway}")
    print(f"[INFO] Red detectada: {network_info.network}")

    return network_info


def resolve_capture_interface(config: dict, network_info=None) -> str:
    interface = config.get("interface", "")

    if not isinstance(interface, str):
        return ""

    if interface.lower() != "auto":
        return interface

    if not network_info:
        print("[AVISO] Se usara la interfaz por defecto de Scapy.")
        return ""

    return network_info.interface


def main():
    print_banner()

    config = load_config("config.json")
    network_info = resolve_network_info(config)
    capture_interface = resolve_capture_interface(config, network_info)
    status_manager = StatusManager(config.get("status_file", "logs/status.json"))
    stop_heartbeat = threading.Event()

    alert_manager = AlertManager(
        log_file=config.get("log_file", "logs/alerts.json"),
        cooldown_seconds=config.get("alert_cooldown_seconds", 0)
    )
    analyzer = TrafficAnalyzer(config, alert_manager, network_info=network_info)

    capture = PacketCapture(
        interface=capture_interface,
        packet_callback=analyzer.analyze_packet
    )

    def heartbeat_loop():
        while not stop_heartbeat.wait(2):
            status_manager.heartbeat()

    try:
        status_manager.start(capture_interface, network_info)
        threading.Thread(target=heartbeat_loop, daemon=True).start()
        capture.start()
    except KeyboardInterrupt:
        print("\n[INFO] IDS detenido por el usuario.")
    except PermissionError:
        print("[ERROR] Ejecuta el programa como administrador/root.")
    except Exception as error:
        print(f"[ERROR] Ocurrió un problema: {error}")
    finally:
        stop_heartbeat.set()
        status_manager.stop()


if __name__ == "__main__":
    main()
