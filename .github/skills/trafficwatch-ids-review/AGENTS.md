# AGENTS.md

Este archivo da instrucciones generales para cualquier asistente de IA que trabaje en este repositorio.

## Proyecto

TrafficWatch IDS es un sistema de deteccion de intrusos con Python, Scapy y Flask. Tiene ejecucion local en Windows y un dashboard de demostracion compatible con Render.

- La ejecucion local captura paquetes, analiza trafico, registra alertas y actualiza estado del IDS.
- El dashboard Flask muestra alertas, incidentes, trafico clasificado, graficos, estado, simulaciones, escaneo local controlado, Suricata IPS y politicas.
- Render es solo para demostracion: puede mostrar dashboard, simulaciones, historial y graficos, pero no debe depender de captura real, Nmap real, Suricata real ni Windows Firewall.

## Primeros Pasos

1. Leer `README.md`, `config.json` y los archivos directamente relacionados con la tarea.
2. Revisar pruebas en `tests/` antes de cambiar reglas IDS, almacenamiento, APIs Flask, dashboard o respuesta activa.
3. Mantener separadas las funciones locales de las funciones compatibles con Render.
4. Tratar `logs/` como datos de ejecucion, no como codigo fuente ni fixtures estables.

## Mapa Rapido

- `main.py`: entrada local del IDS.
- `src/packet_capture.py`: captura con Scapy.
- `src/analyzer.py`: reglas IDS y clasificacion de trafico.
- `src/alert_manager.py`: alertas, cooldown y metadatos de respuesta.
- `src/storage.py`: persistencia JSON tolerante a corrupcion.
- `src/network_utils.py`: deteccion de IP, gateway, red e interfaz.
- `src/status_manager.py`: estado operativo y latidos del IDS.
- `src/network_scanner.py`: escaneo controlado de dispositivos locales.
- `src/real_scan.py`: Nmap local validado.
- `src/response_actions.py`: respuesta activa con Windows Firewall.
- `src/suricata_integration.py`: Suricata EVE, comandos, reglas y planes IPS.
- `web/app.py`: rutas Flask y APIs del dashboard.
- `web/templates/dashboard.html`: interfaz principal.
- `web/templates/attack_lab.html`: laboratorio web controlado.
- `config.json`: umbrales, logs, dashboard, escaneo, Suricata y respuesta activa.
- `docs/`: documentacion academica y despliegue.
- `tests/`: pruebas pytest.

## Reglas de Trabajo

- Preferir cambios pequenos, enfocados y consistentes con el estilo simple del proyecto.
- Mantener umbrales y switches configurables en `config.json`.
- Mantener consistentes los tipos de alerta entre analizador, simulador, dashboard, respuesta activa, pruebas y Suricata.
- Conservar las etiquetas en espanol del dashboard y el tono academico de la documentacion.
- Para cambios en `docs/`, mantener coherencia con README, Render y las funciones reales del sistema.
- No agregar archivos generados, logs locales, capturas, builds o rutas especificas de una maquina.

## Seguridad

- No ejecutar captura real, Nmap real, Suricata real, cambios de firewall, instaladores o scripts de administrador sin pedido explicito del usuario.
- No usar `logs/alerts.json`, `logs/traffic.json`, `logs/status.json`, `logs/policies.json` o `logs/suricata/eve.json` reales como fixtures.
- No romper compatibilidad con Render al agregar funciones que dependan de Windows, red local, permisos de administrador, Nmap, Npcap o Suricata.
- Mantener el bloqueo automatico conservador. Las acciones de firewall deben ser recomendadas o manuales salvo instruccion explicita.

## Validacion

Usar la validacion mas especifica segun el cambio:

```powershell
python -m json.tool config.json
python -m pytest
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
python -m pytest tests/test_storage.py
python -m compileall src web
```

Para cambios solo del dashboard o APIs Flask, preferir `app.test_client()`:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

## Prioridades de Revision

- Alertas duplicadas, ruidosas o con claves de cooldown incorrectas.
- Cambios que rompan agrupacion de incidentes, exportaciones CSV/JSON o renderizado del dashboard.
- Tipos de alerta inconsistentes entre modulos.
- JavaScript que asuma que todos los campos de API existen siempre.
- Pruebas que dependan de red real, logs reales, permisos de administrador o servicios externos.
- Rutas Flask o despliegue Render que asuman herramientas exclusivas de Windows.
