# Instrucciones Para Copilot

Este repositorio es TrafficWatch IDS, un sistema de detección de intrusos con Python/Flask para Windows y con un dashboard de demostración compatible con Render.

## Contexto Del Proyecto

- Ejecución local: `main.py` carga `config.json`, detecta la red local, captura paquetes con Scapy, analiza tráfico, escribe el estado y almacena alertas.
- Ejecución del dashboard: `web/app.py` sirve páginas Flask y APIs para alertas, incidentes, tráfico clasificado, exportaciones, escaneos, simulaciones, ayudantes de Suricata y políticas.
- La lógica de detección vive principalmente en `src/analyzer.py`; el cooldown de alertas y los metadatos de respuesta activa viven en `src/alert_manager.py` y `src/response_actions.py`.
- La captura local vive en `src/packet_capture.py`; el estado operativo vive en `src/status_manager.py`; los escaneos controlados usan `src/network_scanner.py` y `src/real_scan.py`.
- `run_dashboard.py` arranca el dashboard local. `docs/` contiene documentación académica, arquitectura, requerimientos, despliegue Render y guía Suricata IPS.
- Los datos JSON de ejecución pertenecen a `logs/` y no deben tratarse como datos fuente.
- Render es solo para demostración. La captura real de paquetes, Nmap, Suricata y las acciones del Firewall de Windows son funciones de máquina local.

## Guías De Código

- Sigue el estilo simple de Python ya existente. Prefiere funciones claras y diccionarios antes que nuevas abstracciones de framework.
- Mantén los umbrales del IDS y los interruptores de funciones configurables mediante `config.json`.
- Mantén consistentes los nombres de tipos de alerta entre analizador, simulador, dashboard, respuesta activa, pruebas e integración con Suricata.
- Conserva las etiquetas en español del dashboard y el tono de proyecto académico salvo que la tarea sea específicamente reescribir textos.
- Para cambios en `docs/`, conserva la estructura FD01-FD06 y la coherencia con README, Render y las funciones reales del sistema.
- Usa alternativas seguras cuando no estén disponibles herramientas exclusivas de Windows, privilegios de administrador, acceso a red local, Nmap, Npcap o Suricata.
- No ejecutes automáticamente escaneos de red, captura de paquetes, cambios de firewall, instaladores o scripts de administrador salvo que se solicite explícitamente.
- No agregues al código fuente archivos generados, logs locales, capturas, salidas de build o rutas específicas de una máquina.

## Pruebas Y Validación

Para cambios en Python, prefiere primero ejecuciones enfocadas de pytest:

```powershell
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
python -m pytest tests/test_storage.py
```

Para cambios amplios, ejecuta:

```powershell
python -m pytest
python -m json.tool config.json
python -m compileall src web
```

Para cambios en el dashboard, usa el cliente de pruebas de Flask cuando sea posible en vez de iniciar un servidor:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

## Prioridades De Revisión

Al revisar o generar código, prioriza:

- Falsos positivos, exceso de alertas, regresiones de cooldown y umbrales de reglas inconsistentes.
- Registros de alerta que puedan romper la agrupación de incidentes, respuestas API, exportaciones o renderizado del dashboard.
- Comportamiento inseguro de respuesta activa, especialmente comandos del Firewall de Windows o bloqueos automáticos.
- Pruebas que dependan de la red real del desarrollador, logs reales, permisos de administrador o servicios externos.
- Compatibilidad con Render al tocar rutas Flask, archivos de despliegue o herramientas opcionales de red.
- JavaScript del dashboard que asuma que todos los campos de API existen siempre.
- Cambios en documentación que prometan funciones no implementadas o incompatibles con Render.
