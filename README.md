# TrafficWatch IDS

Sistema basico de deteccion de intrusos para Windows, desarrollado con Python, Scapy y Flask.

El proyecto captura trafico de red en tiempo real, genera alertas de seguridad y muestra los resultados en un dashboard web local.

Tambien puede publicarse como dashboard web en Render para demostracion academica.
En Render se visualiza la interfaz, simulaciones, graficos e historial; la captura real
de red, Suricata y el bloqueo IPS deben ejecutarse en una maquina dentro de la red local.

## Enlaces del proyecto

Repositorio GitHub:

```text
https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-i-u3-ids-sistema-deteccion-de-instrusos_u3
```

Demo en Render:

```text
Dashboard: https://proyecto-si784-2026-i-u1-ids.onrender.com/
Simulador atacante: https://proyecto-si784-2026-i-u1-ids.onrender.com/attack-lab
```

Carpeta de evidencias en Google Drive:

```text
https://drive.google.com/drive/folders/1Q2PTs7s7vJ1NTpOqziYL1PbAINZa8mvs
```

Ejecutable Windows:

```text
https://github.com/diegochara2019065026/proyecto-si784-2026-i-u1-ids/releases/tag/v1.0.0-windows
```

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
- Respuesta activa recomendada para IPs con ICMP flood o fuerza bruta SSH.
- Dashboard web con secciones de alertas, historial, graficos, estado del IDS y trafico clasificado.
- Exportacion de alertas en JSON y CSV.
- Exportacion de trafico clasificado en JSON y CSV.

## Componentes principales

| Componente | Archivo / carpeta | Funcion |
|---|---|---|
| Arranque del IDS | `main.py` | Carga la configuracion, detecta la red, inicia la captura y actualiza el estado del IDS. |
| Captura de paquetes | `src/packet_capture.py` | Usa Scapy para capturar paquetes de red. |
| Analisis IDS | `src/analyzer.py` | Clasifica el trafico y aplica las reglas de deteccion. |
| Gestion de alertas | `src/alert_manager.py` | Genera alertas y aplica cooldown para evitar alertas repetidas. |
| Almacenamiento | `src/storage.py` | Guarda y lee informacion en archivos JSON. |
| Utilidades de red | `src/network_utils.py` | Detecta IP local, gateway, red e interfaz; tambien genera ejemplos de pruebas. |
| Estado del IDS | `src/status_manager.py` | Guarda si el IDS esta activo, interfaz usada, red detectada y ultimo latido. |
| Dashboard Flask | `web/app.py` | Expone la web y las APIs locales del dashboard. |
| Interfaz web | `web/templates/dashboard.html` | Muestra tablas, historial, graficos, estado IDS y botones de exportacion. |
| Simulador de fuerza bruta | `simular_fuerza_bruta.py` | Genera conexiones TCP repetidas para pruebas controladas. |
| Configuracion | `config.json` | Define interfaz, logs, cooldown, monitoreo y reglas IDS. |

## Estructura del proyecto

```text
TrafficWatch IDS/
├── docs/                         Documentacion academica FD01-FD05
├── media/                        Recursos visuales del proyecto
├── src/                          Codigo principal del IDS
│   ├── alert_manager.py           Gestion de alertas y cooldown
│   ├── analyzer.py                Reglas IDS y clasificacion de trafico
│   ├── network_utils.py           Deteccion automatica de red y ejemplos
│   ├── packet_capture.py          Captura de paquetes con Scapy
│   ├── status_manager.py          Estado operativo del IDS
│   ├── storage.py                 Persistencia JSON
│   └── utils.py                   Utilidades generales
├── tests/                        Pruebas del proyecto
├── web/                          Dashboard Flask
│   ├── app.py                     Rutas web, APIs y exportaciones
│   └── templates/
│       └── dashboard.html         Interfaz del dashboard
├── config.json                   Configuracion de reglas y logs
├── main.py                       Ejecuta el IDS
├── run_dashboard.py              Ejecuta el dashboard
├── setup_windows.ps1             Setup automatico para Windows
├── abrir_cmd_proyecto.bat        Abre dashboard automaticamente
├── abrir_powershell_admin.bat    Abre IDS como administrador
├── abrir_powershell_pruebas.bat  Abre consola de pruebas
├── powershell_pruebas_loop.ps1   Bucle de ejemplos para pruebas
├── open_admin_powershell.ps1     Elevacion a PowerShell administrador
├── simular_fuerza_bruta.py       Simulador de conexiones repetidas
├── requirements.txt              Dependencias Python
└── README.md                     Guia principal del proyecto
```

La carpeta `logs/` se crea durante la ejecucion, pero esta ignorada por Git para no subir alertas, trafico ni direcciones IP reales.

## Requisitos

- Windows.
- Python 3.9 o superior.
- Nmap instalado.
- Permisos de administrador para ejecutar el IDS principal.

## Modos de uso

El proyecto puede usarse de tres formas:

| Modo | Para que sirve | Funciones disponibles |
|---|---|---|
| Local con Python | Desarrollo y pruebas completas en tu PC | Dashboard, simulador, Nmap local, Suricata local, escaneo de red local |
| Ejecutable Windows | Usar el dashboard sin abrir VS Code ni instalar dependencias manualmente | Dashboard, simulador, laboratorio remoto; Nmap/Suricata si estan instalados en esa PC |
| Render | Demostracion web publica | Dashboard, simulador, historial y graficos; no captura red local ni ejecuta Nmap/Suricata reales |

## Ejecutable Windows

El ejecutable esta publicado como release en GitHub:

```text
https://github.com/diegochara2019065026/proyecto-si784-2026-i-u1-ids/releases/tag/v1.0.0-windows
```

Pasos:

1. Descarga `TrafficWatchIDS-Windows.zip`.
2. Descomprime el archivo ZIP.
3. Entra a la carpeta `TrafficWatchIDS`.
4. Ejecuta `TrafficWatchIDS.exe`.
5. El dashboard abrira automaticamente en:

   ```text
   http://127.0.0.1:5000/
   ```

6. El simulador atacante estara en:

   ```text
   http://127.0.0.1:5000/attack-lab
   ```

Para que otra PC de la misma red entre al dashboard, usa la IP de la PC donde esta corriendo el ejecutable:

```text
http://<IP-DE-LA-PC>:5000/
http://<IP-DE-LA-PC>:5000/attack-lab
```

Ejemplo:

```text
http://192.168.100.10:5000/
http://192.168.100.10:5000/attack-lab
```

Nota: si Windows Firewall pregunta, permite el acceso en red privada.

### Crear nuevamente el ejecutable

Si se modifica el codigo y se quiere generar otro ejecutable:

```powershell
CREAR_EJECUTABLE_WINDOWS.bat
```

El archivo generado queda en:

```text
dist/TrafficWatchIDS/TrafficWatchIDS.exe
```

### Crear instalador Windows

Si quieres entregar el proyecto como instalador para cualquier computadora Windows:

```powershell
CREAR_INSTALADOR_WINDOWS.bat
```

Ese comando:

- Crea primero `TrafficWatchIDS.exe` si todavia no existe.
- Usa Inno Setup para generar un instalador profesional.
- Si Inno Setup no esta instalado, puede instalarlo con `winget`.
- Genera el archivo final en:

```text
installer_output/TrafficWatchIDS_Setup.exe
```

En la otra computadora solo se ejecuta:

```text
TrafficWatchIDS_Setup.exe
```

Despues de instalar, se abre `TrafficWatch IDS` desde el acceso directo del escritorio o desde el menu Inicio.

Durante la instalacion puedes marcar estas herramientas opcionales:

- `Instalar Nmap y Npcap`: descarga Nmap mediante `winget`; habilita escaneos reales y captura de red.
- `Instalar Python 3.12`: descarga Python mediante `winget`; util para ejecutar scripts, modificar o desarrollar el proyecto.

Ambas requieren conexion a Internet, `winget` y aceptar la solicitud de administrador. El dashboard empaquetado funciona sin marcar Python.

Nota: el dashboard empaquetado no necesita que el usuario instale Flask ni Python manualmente para abrirlo. Para funciones reales de red, Nmap y Npcap siguen siendo dependencias externas opcionales:

- Nmap: necesario para escaneo real de puertos.
- Npcap: necesario para captura IDS real con Scapy.

El instalador agrega una opcion llamada `Instalar dependencias opcionales` para revisar o instalar esas herramientas.

## Despliegue web en Render

El proyecto incluye `render.yaml`, `runtime.txt` y `gunicorn` para desplegar el dashboard.

Configuracion principal:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn web.app:app --bind 0.0.0.0:$PORT
```

Guia completa:

```text
docs/DEPLOY_RENDER.md
```

## Laboratorio remoto en red local

El dashboard incluye una pagina para que otro integrante conectado a la misma red
genere eventos de laboratorio desde su propio equipo:

```text
http://<IP-DE-TU-PC>:5000/attack-lab
```

Ejemplo:

```text
http://192.168.100.10:5000/attack-lab
```

Cuando el integrante presiona un boton, el dashboard registra una alerta con la IP
del equipo que hizo la solicitud. Para que otras PCs entren, inicia el dashboard con:

```powershell
python run_dashboard.py
```

Si Windows Firewall pregunta, permite el acceso en red privada.

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

## Instalacion recomendada en Windows

Para instalar el proyecto en otra computadora Windows:

1. Descargar el repositorio desde GitHub como ZIP o clonarlo con Git.
2. Descomprimirlo en una carpeta simple, por ejemplo:

   ```text
   C:\TrafficWatchIDS
   ```

3. Abrir PowerShell en esa carpeta.
4. Ejecutar:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\INSTALAR_TRAFFICWATCH_WINDOWS.ps1
   ```

El instalador:

- Verifica Python 3.
- Crea un entorno virtual `.venv`.
- Instala dependencias desde `requirements.txt`.
- Crea carpetas de logs.
- Crea una regla de firewall para el puerto `5000` en red privada.
- Crea un acceso directo en el escritorio llamado `TrafficWatch IDS`.
- Crea un acceso directo `TrafficWatch IDS Captura` para iniciar la captura como administrador.
- Verifica si Nmap y Suricata estan disponibles.
- Si Nmap no esta instalado, pregunta si deseas instalarlo automaticamente con `winget`.
- Verifica Npcap; si falta, pregunta si deseas abrir la pagina oficial de descarga.

Luego se puede iniciar con:

```text
INICIAR_TRAFFICWATCH.bat
```

o con el acceso directo del escritorio.

Para captura IDS real con Scapy:

```text
TrafficWatch IDS Captura
```

Ese acceso directo abre PowerShell como administrador y ejecuta:

```powershell
python main.py
```

La captura real necesita Npcap instalado. Si no esta instalado, el instalador puede abrir:

```text
https://npcap.com/#download
```

En la computadora donde corre el dashboard:

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/attack-lab
```

Desde otra PC o celular en la misma red:

```text
http://<IP-DE-LA-PC>:5000/
http://<IP-DE-LA-PC>:5000/attack-lab
```

El sistema detecta automaticamente la IP local para mostrar la URL de red y para iniciar Suricata si esta instalado.

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

## Respuesta activa ante IP sospechosa

El proyecto puede agregar una accion de respuesta junto a las alertas criticas.
Por defecto no bloquea automaticamente: recomienda el bloqueo y muestra el comando
de Windows Firewall dentro del registro de la alerta.

Configuracion en `config.json`:

```json
"active_response": {
    "enabled": true,
    "auto_block_enabled": false,
    "block_minutes": 10,
    "block_alert_types": [
        "ICMP_FLOOD",
        "FUERZA_BRUTA_SSH"
    ],
    "windows_firewall_rule_prefix": "TrafficWatch IDS Auto Block"
}
```

Con `auto_block_enabled` en `false`, el dashboard registra:

```text
Respuesta: RECOMENDADO (2 min, configuracion actual de prueba)
```

Con `auto_block_enabled` en `true`, el IDS intenta crear una regla de Windows
Firewall automaticamente. Para eso debe ejecutarse como administrador.

En el Dashboard, las alertas `FUERZA_BRUTA_SSH` y las pruebas controladas
`TRAFICO_REAL_LAB_FUERZA_BRUTA_SSH` incluyen el boton `Bloquear 2 min`.
Este crea una regla de entrada en Windows Firewall para la IP origen y la
elimina automaticamente al terminar los diez minutos. Inicia
TrafficWatch como administrador para que el boton pueda funcionar. La regla
protege solamente la PC que ejecuta TrafficWatch; no desconecta al usuario del
Wi-Fi ni bloquea su acceso a otros dispositivos.

Comando equivalente:

```powershell
New-NetFirewallRule -DisplayName "TrafficWatch IDS Auto Block FUERZA_BRUTA_SSH 192.168.1.50" -Direction Inbound -RemoteAddress 192.168.1.50 -Action Block
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

## Calidad y seguridad en GitHub

El repositorio incluye workflows de GitHub Actions para pruebas, reportes en GitHub Pages y analisis estatico.

Reportes publicados:

```text
https://upt-faing-epis.github.io/proyecto-si784-2026-i-u3-ids-sistema-deteccion-de-instrusos_u3/
```

Secciones principales:

- Pruebas unitarias, cobertura, BDD, interfaz y mutacion.
- Analisis Estatico Detallado con SonarCloud, Semgrep y Snyk.
- Escaneo en SonarCloud desde GitHub Actions.

Configuracion complementaria:

```text
docs/QA_ANALISIS_ESTATICO.md
sonar-project.properties
```

## Importante sobre permisos

- `python main.py` necesita permisos de administrador porque captura paquetes de red.
- `python run_dashboard.py` no necesita permisos de administrador.
- Las pruebas con Nmap deben hacerse solo contra equipos o redes propias/autorizadas.

## Uso etico

Este sistema debe usarse solo en redes propias, laboratorios academicos o entornos donde tengas autorizacion explicita.

No uses este proyecto para escanear, probar o atacar redes de terceros.
