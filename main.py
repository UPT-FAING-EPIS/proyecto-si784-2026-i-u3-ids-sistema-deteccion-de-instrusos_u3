from src.packet_capture import PacketCapture
from src.analyzer import TrafficAnalyzer
from src.alert_manager import AlertManager
from src.utils import load_config, print_banner


def main():
    print_banner()

    config = load_config("config.json")
    alert_manager = AlertManager(config.get("log_file", "logs/alerts.json"))
    analyzer = TrafficAnalyzer(config, alert_manager)

    capture = PacketCapture(
        interface=config.get("interface", ""),
        packet_callback=analyzer.analyze_packet
    )

    try:
        capture.start()
    except KeyboardInterrupt:
        print("\n[INFO] IDS detenido por el usuario.")
    except PermissionError:
        print("[ERROR] Ejecuta el programa como administrador/root.")
    except Exception as error:
        print(f"[ERROR] Ocurrió un problema: {error}")


if __name__ == "__main__":
    main()
