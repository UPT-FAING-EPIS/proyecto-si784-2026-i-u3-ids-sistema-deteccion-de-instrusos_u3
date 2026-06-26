---
name: trafficwatch-ids-review
description: Skill específica para revisar e implementar cambios en TrafficWatch IDS, un proyecto de detección de intrusos con Python y Flask. Úsala cuando se solicite revisar, modificar, probar, documentar, empaquetar o solucionar problemas de este repositorio, incluyendo reglas del analizador, almacenamiento de alertas, respuesta activa, utilidades de red, APIs del dashboard Flask, integración con Suricata, scripts de Windows, despliegue en Render, pruebas y documentación académica.
---

# Revisión De TrafficWatch IDS

## Propósito

Usa esta skill para trabajar dentro del repositorio TrafficWatch IDS teniendo en cuenta sus restricciones de seguridad, red, dashboard, empaquetado para Windows y demostración académica.

## Primer Paso

1. Lee `README.md`, `config.json` y los archivos directamente relacionados con la solicitud.
2. Revisa las pruebas existentes en `tests/` antes de cambiar la detección, el almacenamiento, la respuesta activa o el comportamiento del dashboard.
3. Conserva la separación actual entre la ejecución local del IDS y la ejecución de demostración en Render.
4. Trata `logs/` como datos de ejecución. No dependas de contenidos de logs versionados.

## Mapa Del Proyecto

- `main.py`: punto de entrada local del IDS. Carga la configuración, detecta información de red, inicia la captura y actualiza el estado.
- `src/analyzer.py`: clasificación de paquetes y reglas IDS para escaneo de puertos, ICMP flood, SYN flood, fuerza bruta, frecuencia de conexiones, puertos sospechosos y puertos raros.
- `src/alert_manager.py`: creación de alertas, cooldown, categorías y metadatos opcionales de respuesta activa.
- `src/storage.py`: persistencia JSON con límite de registros y lectura tolerante a corrupción.
- `src/network_utils.py`: detección de red en Windows y ejemplos de comandos.
- `src/response_actions.py`: respuesta activa con Firewall de Windows. Mantén el bloqueo automático de forma conservadora.
- `src/suricata_integration.py`: estado de Suricata, alertas de demostración, reglas locales, planes IPS y constructores de comandos de firewall.
- `web/app.py`: rutas Flask, endpoints API, agregación del dashboard, exportaciones, simulación, escaneos y políticas.
- `web/templates/dashboard.html`: interfaz principal del dashboard.
- `web/templates/attack_lab.html`: interfaz controlada del laboratorio de ataques.
- `suricata/local.rules`: reglas locales de Suricata.
- `config.json`: umbrales, rutas de logs, ventana del dashboard, límites de escaneo de red, Suricata y configuración de respuesta activa.
- `tests/`: cobertura enfocada con pytest para clasificación del analizador, almacenamiento, alertas, utilidades de red y respuesta activa.
- Scripts de Windows: configuración, lanzador, empaquetado, instalador y ayudantes de administrador.
- `render.yaml` y `runtime.txt`: despliegue de demostración en Render.

## Reglas De Trabajo

- Prefiere cambios pequeños y enfocados que mantengan el estilo actual de Python simple.
- Mantén los umbrales de detección configurables en `config.json` en vez de fijar constantes de seguridad directamente en el código.
- Agrega o actualiza pruebas cuando cambies tipos de alerta, comportamiento de reglas, formatos de almacenamiento, respuestas de APIs Flask o generación de comandos de respuesta activa.
- Mantén las funciones solo locales con alternativas seguras para Render. Render puede mostrar el dashboard, simulaciones, historial y gráficos, pero no puede capturar paquetes locales, ejecutar Nmap/Suricata reales ni modificar el Firewall de Windows.
- Evita escaneos reales de red, captura de paquetes, ejecución de Suricata, cambios de firewall, instaladores o scripts de administrador salvo que el usuario lo pida explícitamente.
- Usa `app.test_client()` de Flask para revisar endpoints cuando no sea necesario abrir un navegador o iniciar un servidor completo.
- Conserva las etiquetas en español ya presentes en el dashboard y la documentación.
- No hagas commits ni crees fixtures a partir de `logs/alerts.json`, `logs/traffic.json`, `logs/status.json`, `logs/policies.json` o `logs/suricata/eve.json` reales.

## Validación

Usa la validación más específica que corresponda al cambio:

```powershell
python -m json.tool config.json
python -m pytest
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
python -m compileall src web
```

Para cambios solo del dashboard, prefiere una prueba rápida con Flask:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

Para cambios de empaquetado, inspecciona el `.bat`, `.ps1`, `installer/TrafficWatchIDS.iss` o la ruta del comando de PyInstaller afectada antes de ejecutarlo. Construir instaladores puede descargar dependencias o requerir herramientas de administrador, así que pregunta antes de ejecutar esos flujos.

## Lista De Revisión

Al revisar un cambio, busca primero:

- Reglas que puedan generar alertas duplicadas o ruidosas porque cambiaron las claves de cooldown.
- Registros de alerta que rompan la agregación del dashboard o la exportación CSV/JSON.
- Nombres de tipos de alerta inconsistentes entre analizador, simulador, respuesta activa, dashboard y ayudantes de Suricata.
- Acciones de bloqueo o escaneo que podrían ejecutarse automáticamente en vez de mantenerse como recomendadas/manuales.
- Pruebas que escriban fuera de `tmp_path` o dependan del estado real de red de la máquina local.
- JavaScript del dashboard que asuma que un campo de API siempre existe.
- Rutas de Render que asuman que existen herramientas exclusivas de Windows.
