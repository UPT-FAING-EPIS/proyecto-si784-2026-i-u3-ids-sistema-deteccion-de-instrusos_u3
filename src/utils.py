import json
from pathlib import Path


def load_config(path: str) -> dict:
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def print_banner():
    print("=" * 68)
    print(" IDS PRO - SISTEMA BÁSICO DE DETECCIÓN DE INTRUSOS")
    print(" Monitoreo de tráfico de red con Python, Scapy y Flask")
    print("=" * 68)
    print("[INFO] Iniciando captura de paquetes...")
    print("[INFO] Presiona CTRL + C para detener.\n")
