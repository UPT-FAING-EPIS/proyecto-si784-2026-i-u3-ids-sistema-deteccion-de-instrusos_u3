# IDS PRO - Sistema Básico de Detección de Intrusos

Versión PRO del proyecto académico IDS para monitoreo de tráfico de red.

## Funciones

- Captura de paquetes en tiempo real con Scapy
- Detección de escaneo de puertos
- Detección de ICMP flood
- Detección de SYN flood
- Detección de intentos repetidos SSH
- Detección de puertos sospechosos
- Alertas en JSON
- Dashboard web con Flask
- Estadísticas por tipo de alerta e IP sospechosa

## Requisitos

- Python 3.9 o superior
- Permisos de administrador/root para capturar paquetes

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar el IDS

### Windows

Abre PowerShell o CMD como administrador:

```bash
python main.py
```

### Linux/macOS

```bash
sudo python3 main.py
```

## Ejecutar el dashboard

En otra terminal:

```bash
python run_dashboard.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

## Configurar interfaz de red

Edita `config.json`:

```json
"interface": "Wi-Fi"
```

Si no sabes el nombre de tu interfaz, deja vacío:

```json
"interface": ""
```

## Logs

Las alertas se guardan en:

```text
logs/alerts.json
```

## Pruebas sugeridas en laboratorio

Generar tráfico normal:
- Abrir páginas web
- Hacer ping a una IP autorizada

Simular escaneo de puertos con autorización:

```bash
nmap -p 1-100 192.168.1.1
```

## Uso ético

Este sistema debe ejecutarse solo en redes propias, laboratorios académicos o entornos donde tengas autorización.
