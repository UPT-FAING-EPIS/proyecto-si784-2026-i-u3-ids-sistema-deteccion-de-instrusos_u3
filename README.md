# TrafficWatch IDS

Sistema basico de deteccion de intrusos para Windows, desarrollado con Python, Scapy y Flask.

El proyecto captura trafico de red en tiempo real, genera alertas de seguridad y muestra los resultados en un dashboard web local.

## Funciones principales

- Captura de paquetes en tiempo real con Scapy.
- Deteccion de escaneo de puertos.
- Deteccion de ICMP flood.
- Deteccion de SYN flood.
- Deteccion de fuerza bruta hacia FTP, SSH, Telnet y RDP.
- Deteccion de alta frecuencia de conexiones.
- Deteccion de puertos sospechosos.
- Deteccion de puertos raros configurados.
- Cooldown de alertas repetidas para evitar ruido.
- Deteccion automatica de IP local, gateway, red e interfaz.
- Clasificacion de trafico: entrante, saliente, local, gateway y externo.
- Dashboard web con secciones de alertas, historial, graficos, estado del IDS y trafico clasificado.
- Exportacion de alertas en JSON y CSV.
- Exportacion de trafico clasificado en JSON y CSV.

## Requisitos

- Windows.
- Python 3.9 o superior.
- Nmap instalado.
- Permisos de administrador para ejecutar el IDS principal.

Nmap puede instalarse desde:

```text
https://nmap.org/download.html#windows
```

Tambien puedes usar el script de setup del proyecto para verificar dependencias.

## Instalacion rapida

Desde la carpeta del proyecto:

```powershell
.\setup_windows.ps1
```

Tambien puedes ejecutarlo desde la terminal integrada de VS Code. Solo abre la terminal dentro del proyecto y escribe el mismo comando.

Este script:

- Verifica Python.
- Verifica pip.
- Instala las dependencias desde `requirements.txt` si faltan.
- Verifica si Nmap esta disponible.
- Si Nmap no esta instalado, intenta instalarlo automaticamente con `winget`.

## Uso rapido con archivos `.bat`

Los archivos `.bat` ya ejecutan los comandos automaticamente. No necesitas escribir `python run_dashboard.py` ni `python main.py` si usas estos accesos.

Para que todo funcione correctamente, abre los archivos o ejecuta los comandos desde el directorio del proyecto.

Si estas en VS Code:

1. Haz clic derecho sobre el archivo `.bat`.
2. Selecciona `Reveal in File Explorer`.
3. En el Explorador de archivos de Windows, haz doble clic sobre el `.bat`.

### Orden recomendado

1. Abre `abrir_cmd_proyecto.bat`.

   Inicia automaticamente el dashboard con `python run_dashboard.py`.

   Luego entra en el navegador a:

   ```text
   http://127.0.0.1:5000
   ```

2. Abre `abrir_powershell_admin.bat`.

   Windows pedira permisos de administrador. Debes aceptar.

   Despues ejecuta automaticamente `python main.py` y empieza a capturar paquetes. Deja esa ventana abierta mientras quieras monitorear la red.

3. Abre `abrir_powershell_pruebas.bat`.

   No necesita permisos de administrador. Sirve para mostrar ejemplos segun tu red detectada y ejecutar pruebas como Nmap, fuerza bruta simulada, alta frecuencia de conexiones y puertos raros.

Con ese orden:

- El dashboard ya esta disponible.
- El IDS ya esta capturando paquetes.
- Las pruebas pueden aparecer como alertas en el dashboard.

## Ejecucion manual opcional

Si prefieres hacerlo manualmente:

### 1. Ejecutar dashboard

```powershell
python run_dashboard.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

### 2. Ejecutar IDS

Abre PowerShell como administrador y ejecuta:

```powershell
python main.py
```

### 3. Ver ejemplos de pruebas

```powershell
python -m src.network_utils
```

Tambien puedes mostrar solo ejemplos:

```powershell
python -m src.network_utils --examples-only --shell powershell
```

## Dashboard

El dashboard incluye estas secciones:

- **Dashboard**: resumen de alertas actuales.
- **Tipos de trafico**: explicacion de trafico entrante, saliente, local y gateway.
- **Trafico clasificado**: ultimos paquetes observados por el IDS.
- **Estado IDS**: muestra si el IDS esta activo, interfaz usada, IP local, gateway, red detectada, ultima alerta y ultimo paquete.
- **Graficos**: alertas por tipo, nivel, minuto y top IPs sospechosas.
- **Historial**: alertas guardadas con filtros, paginacion y exportacion.
- **Reglas IDS**: resumen de reglas activas.

## Reglas IDS configuradas

Las reglas estan en `config.json`.

Actualmente el proyecto puede generar alertas como:

```text
ESCANEO_DE_PUERTOS
SYN_FLOOD
ICMP_FLOOD
PUERTO_SOSPECHOSO
PUERTO_RARO
ALTA_FRECUENCIA_CONEXIONES
FUERZA_BRUTA_FTP
FUERZA_BRUTA_SSH
FUERZA_BRUTA_TELNET
FUERZA_BRUTA_RDP
```

## Archivos de logs

Las alertas se guardan en:

```text
logs/alerts.json
```

El trafico clasificado se guarda en:

```text
logs/traffic.json
```

El estado del IDS se guarda en:

```text
logs/status.json
```

## Exportaciones

Desde el dashboard puedes exportar:

Alertas:

```text
/api/export/alerts.json
/api/export/alerts.csv
```

Trafico clasificado:

```text
/api/export/traffic.json
/api/export/traffic.csv
```

## Pruebas sugeridas

Primero ejecuta:

```powershell
python -m src.network_utils
```

El sistema detectara tu red y mostrara ejemplos para:

- Escaneo de puertos con Nmap.
- Fuerza bruta simulada.
- Alta frecuencia de conexiones.
- Puertos raros.

Ejemplos generales:

```powershell
nmap -p 1-100 <gateway>
python simular_fuerza_bruta.py --port 21 --count 10
python simular_fuerza_bruta.py --port 3389 --count 10
python simular_fuerza_bruta.py --port 80 --count 120 --delay 0.01
nmap -p 31337 <gateway>
```

Si no pasas `--host` en `simular_fuerza_bruta.py`, el script usa automaticamente el gateway detectado.

## Importante sobre permisos

- `python main.py` necesita permisos de administrador porque captura paquetes de red.
- `python run_dashboard.py` no necesita permisos de administrador.
- Las pruebas con Nmap deben hacerse solo contra equipos o redes propias/autorizadas.

## Uso etico

Este sistema debe usarse solo en redes propias, laboratorios academicos o entornos donde tengas autorizacion explicita.

No uses este proyecto para escanear, probar o atacar redes de terceros.
