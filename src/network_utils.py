import argparse
import ipaddress
import json
import platform
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NetworkInfo:
    interface: str
    interface_index: int
    ip_address: str
    prefix_length: int
    gateway: str
    network: str


def _first_value(value):
    if isinstance(value, list):
        return value[0] if value else None

    return value


def _build_network(ip_address: str, prefix_length: int) -> str:
    network = ipaddress.ip_network(f"{ip_address}/{prefix_length}", strict=False)
    return str(network)


def _network_info_from_adapter(adapter: dict) -> NetworkInfo:
    ip_address = _first_value(adapter.get("IPAddress"))
    prefix_length = _first_value(adapter.get("PrefixLength"))
    gateway = _first_value(adapter.get("Gateway"))
    interface = _first_value(adapter.get("InterfaceAlias"))
    interface_index = _first_value(adapter.get("InterfaceIndex"))

    if not ip_address or prefix_length is None or not gateway or not interface:
        raise ValueError("No se pudo leer una configuracion IPv4 completa.")

    prefix_length = int(prefix_length)
    interface_index = int(interface_index or 0)

    return NetworkInfo(
        interface=str(interface),
        interface_index=interface_index,
        ip_address=str(ip_address),
        prefix_length=prefix_length,
        gateway=str(gateway),
        network=_build_network(str(ip_address), prefix_length),
    )


def _run_windows_network_query() -> dict:
    powershell_script = """
    $adapter = Get-NetIPConfiguration |
        Where-Object { $_.IPv4Address -and $_.IPv4DefaultGateway } |
        Select-Object -First 1

    if ($null -eq $adapter) {
        exit 2
    }

    [PSCustomObject]@{
        InterfaceAlias = $adapter.InterfaceAlias
        InterfaceIndex = $adapter.InterfaceIndex
        IPAddress = @($adapter.IPv4Address)[0].IPAddress
        PrefixLength = @($adapter.IPv4Address)[0].PrefixLength
        Gateway = @($adapter.IPv4DefaultGateway)[0].NextHop
    } | ConvertTo-Json -Compress
    """

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            powershell_script,
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo detectar la red activa en Windows. "
            "Verifica que exista una conexion IPv4 con gateway."
        )

    output = result.stdout.strip()

    if not output:
        raise RuntimeError("Windows no devolvio informacion de red.")

    return json.loads(output)


def detect_network_info() -> NetworkInfo:
    if platform.system() != "Windows":
        raise RuntimeError("La deteccion automatica de red esta optimizada para Windows.")

    adapter = _run_windows_network_query()
    return _network_info_from_adapter(adapter)


def get_port_scan_examples(network_info: NetworkInfo) -> List[str]:
    return [
        f"nmap -p 1-100 {network_info.gateway}",
        f"nmap -p 1-1000 {network_info.gateway}",
        f"nmap --top-ports 20 {network_info.gateway}",
        f"nmap -sT -Pn -p 22,23,53,80,443,3389 {network_info.gateway}",
        f"nmap -sV {network_info.gateway}",
        f"nmap -O {network_info.gateway}",
        f"nmap -A {network_info.gateway}",
        f"nmap -sn {network_info.network}",
    ]


def get_brute_force_examples(network_info: NetworkInfo, shell: str = "powershell") -> List[str]:
    if shell == "cmd":
        return [
            f"for /L %i in (1,1,5) do @cmd /c \"python simular_fuerza_bruta.py --host {network_info.gateway} --port 21 --count 10 & timeout /t 11 /nobreak > nul\"",
            f"for /L %i in (1,1,5) do @cmd /c \"python simular_fuerza_bruta.py --host {network_info.gateway} --port 22 --count 10 & timeout /t 11 /nobreak > nul\"",
            f"for /L %i in (1,1,5) do @cmd /c \"python simular_fuerza_bruta.py --host {network_info.gateway} --port 23 --count 10 & timeout /t 11 /nobreak > nul\"",
            f"for /L %i in (1,1,5) do @cmd /c \"python simular_fuerza_bruta.py --host {network_info.gateway} --port 3389 --count 10 & timeout /t 11 /nobreak > nul\"",
        ]

    return [
        f"for ($i=1; $i -le 5; $i++) {{ python simular_fuerza_bruta.py --host {network_info.gateway} --port 21 --count 10; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 5; $i++) {{ python simular_fuerza_bruta.py --host {network_info.gateway} --port 22 --count 10; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 5; $i++) {{ python simular_fuerza_bruta.py --host {network_info.gateway} --port 23 --count 10; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 5; $i++) {{ python simular_fuerza_bruta.py --host {network_info.gateway} --port 3389 --count 10; Start-Sleep -Seconds 11 }}",
    ]


def get_connection_frequency_examples(network_info: NetworkInfo) -> List[str]:
    return [
        f"python simular_fuerza_bruta.py --host {network_info.gateway} --port 80 --count 120 --delay 0.01",
        f"python simular_fuerza_bruta.py --host {network_info.gateway} --port 443 --count 120 --delay 0.01",
        f"python simular_fuerza_bruta.py --host {network_info.gateway} --port 53 --count 120 --delay 0.01",
        f"python simular_fuerza_bruta.py --host {network_info.gateway} --port 8080 --count 120 --delay 0.01",
    ]


def get_rare_port_examples(network_info: NetworkInfo) -> List[str]:
    return [
        f"for ($i=1; $i -le 3; $i++) {{ nmap -p 31337 {network_info.gateway}; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 3; $i++) {{ nmap -p 6667 {network_info.gateway}; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 3; $i++) {{ nmap -p 9001 {network_info.gateway}; Start-Sleep -Seconds 11 }}",
        f"for ($i=1; $i -le 3; $i++) {{ nmap -p 1337 {network_info.gateway}; Start-Sleep -Seconds 11 }}",
    ]


def _ask_example_count(default_count: int, max_count: int) -> int:
    try:
        raw_value = input(f"\nCuantos ejemplos quieres ver por tipo? [{default_count}]: ").strip()
    except EOFError:
        return default_count

    if not raw_value:
        return default_count

    try:
        example_count = int(raw_value)
    except ValueError:
        print(f"Valor no valido. Se mostraran {default_count} ejemplos.")
        return default_count

    if example_count < 1:
        print(f"El numero debe ser mayor que 0. Se mostraran {default_count} ejemplos.")
        return default_count

    return min(example_count, max_count)


def format_network_info(
    network_info: NetworkInfo,
    example_count: Optional[int] = None,
    include_network_info: bool = True,
    shell: str = "powershell",
) -> str:
    port_scan_examples = get_port_scan_examples(network_info)
    brute_force_examples = get_brute_force_examples(network_info, shell=shell)
    connection_frequency_examples = get_connection_frequency_examples(network_info)
    rare_port_examples = get_rare_port_examples(network_info)

    if example_count is None:
        example_count = max(
            len(port_scan_examples),
            len(brute_force_examples),
            len(connection_frequency_examples),
            len(rare_port_examples),
        )

    selected_port_scan_examples = port_scan_examples[:example_count]
    selected_brute_force_examples = brute_force_examples[:example_count]
    selected_connection_frequency_examples = connection_frequency_examples[:example_count]
    selected_rare_port_examples = rare_port_examples[:example_count]

    lines = []

    if include_network_info:
        lines.extend([
            f"Interfaz activa: {network_info.interface}",
            f"Indice de interfaz: {network_info.interface_index}",
            f"IP local: {network_info.ip_address}",
            f"Prefijo: /{network_info.prefix_length}",
            f"Gateway: {network_info.gateway}",
            f"Red detectada: {network_info.network}",
            "",
        ])

    lines.extend([
        f"Ejemplos para ESCANEO_DE_PUERTOS ({len(selected_port_scan_examples)}):",
        *selected_port_scan_examples,
        "",
        f"Ejemplos para FUERZA_BRUTA ({len(selected_brute_force_examples)}):",
        *selected_brute_force_examples,
        "",
        f"Ejemplos para ALTA_FRECUENCIA_CONEXIONES ({len(selected_connection_frequency_examples)}):",
        *selected_connection_frequency_examples,
        "",
        f"Ejemplos para PUERTO_RARO ({len(selected_rare_port_examples)}):",
        *selected_rare_port_examples,
        "",
        f"Nota: los ejemplos de FUERZA_BRUTA son para {shell.upper()} y ejecutan 5 bloques de 10 intentos.",
    ])

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detecta la red actual y muestra ejemplos de prueba.")
    parser.add_argument(
        "--examples-only",
        action="store_true",
        help="Muestra solo ejemplos, sin datos de interfaz/IP/gateway."
    )
    parser.add_argument(
        "--shell",
        choices=["cmd", "powershell"],
        default="powershell",
        help="Formato de los ejemplos de fuerza bruta."
    )

    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    info = detect_network_info()
    max_examples = max(
        len(get_port_scan_examples(info)),
        len(get_brute_force_examples(info, shell=args.shell)),
        len(get_connection_frequency_examples(info)),
        len(get_rare_port_examples(info)),
    )
    count = _ask_example_count(default_count=3, max_count=max_examples)
    print()
    print(format_network_info(
        info,
        example_count=count,
        include_network_info=not args.examples_only,
        shell=args.shell,
    ))
