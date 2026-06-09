import argparse
import socket
import time
from typing import Optional

from src.network_utils import detect_network_info


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    3389: "RDP",
}


def positive_int(value: str) -> int:
    number = int(value)

    if number <= 0:
        raise argparse.ArgumentTypeError("El valor debe ser mayor que 0.")

    return number


def valid_port(value: str) -> int:
    port = positive_int(value)

    if port > 65535:
        raise argparse.ArgumentTypeError("El puerto debe estar entre 1 y 65535.")

    return port


def non_negative_float(value: str) -> float:
    number = float(value)

    if number < 0:
        raise argparse.ArgumentTypeError("El valor no puede ser negativo.")

    return number


def resolve_target_host(host: Optional[str]) -> str:
    if host:
        return host

    network_info = detect_network_info()
    return network_info.gateway


def simulate_connections(host: str, port: int, count: int, delay: float, timeout: float):
    successful_attempts = 0
    failed_attempts = 0
    service = COMMON_PORTS.get(port, "SERVICIO")

    print("[INFO] Simulacion de patron de fuerza bruta")
    print(f"[INFO] Objetivo: {host}")
    print(f"[INFO] Servicio: {service}")
    print(f"[INFO] Puerto: {port}")
    print(f"[INFO] Intentos: {count}")
    print("[INFO] No se envian usuarios ni contrasenas; solo conexiones TCP.\n")

    for attempt_number in range(1, count + 1):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                successful_attempts += 1
                status = "conexion aceptada"
        except OSError as error:
            failed_attempts += 1
            status = f"conexion fallida ({error.__class__.__name__})"

        print(f"[{attempt_number}/{count}] {host}:{port} -> {status}")

        if attempt_number < count and delay > 0:
            time.sleep(delay)

    print("\n[RESUMEN]")
    print(f"Intentos exitosos: {successful_attempts}")
    print(f"Intentos fallidos: {failed_attempts}")
    print("Revisa el dashboard para ver si se genero FUERZA_BRUTA_*.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Simula conexiones TCP repetidas hacia un puerto comun para probar "
            "la regla de fuerza bruta del IDS en un entorno autorizado."
        )
    )
    parser.add_argument(
        "--host",
        help="IP objetivo. Si se omite, se usa el gateway detectado automaticamente."
    )
    parser.add_argument(
        "--port",
        required=True,
        type=valid_port,
        help="Puerto objetivo, por ejemplo 21, 22, 23 o 3389."
    )
    parser.add_argument(
        "--count",
        type=positive_int,
        default=10,
        help="Cantidad de intentos TCP a realizar. Valor por defecto: 10."
    )
    parser.add_argument(
        "--delay",
        type=non_negative_float,
        default=0.2,
        help="Espera en segundos entre intentos. Valor por defecto: 0.2."
    )
    parser.add_argument(
        "--timeout",
        type=non_negative_float,
        default=1.0,
        help="Timeout de conexion en segundos. Valor por defecto: 1.0."
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    host = resolve_target_host(args.host)

    simulate_connections(
        host=host,
        port=args.port,
        count=args.count,
        delay=args.delay,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
