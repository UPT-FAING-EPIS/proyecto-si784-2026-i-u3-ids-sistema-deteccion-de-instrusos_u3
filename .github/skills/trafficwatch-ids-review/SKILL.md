---
name: trafficwatch-ids-review
description: Skill especifica para entender, comparar, revisar, implementar, probar y documentar TrafficWatch IDS, un sistema academico de deteccion de intrusos con Python, Flask, Scapy, dashboard web, respuesta activa controlada, Suricata/IPS, scripts de Windows y despliegue demo en Render. Usala cuando el usuario pregunte que existe en el proyecto, pida resumenes, comparaciones entre codigo y documentacion, auditorias de APIs, reglas IDS, alertas, trafico clasificado, dashboard, red local, bloqueo temporal, pruebas, empaquetado, documentacion o compatibilidad Render/local.
---

# Revision de TrafficWatch IDS

## Proposito

Usa esta skill para trabajar dentro del repositorio TrafficWatch IDS con contexto de seguridad, red local, dashboard, despliegue academico y compatibilidad Windows/Render.

La prioridad es mantener el sistema util para laboratorio, demostrable en Render y seguro para pruebas controladas. No conviertas funciones de simulacion o defensa en acciones ofensivas ni automatices acciones de red sin autorizacion explicita del usuario.

## Uso Conversacional

La skill tambien sirve para preguntas de entendimiento, no solo para editar codigo. Si el usuario pide "que hace el proyecto", "compara esto con aquello", "que existe en el repo" o "segun la skill revisa...", responde usando el mapa del proyecto y leyendo los archivos relevantes.

Ejemplos naturales:

- `Usa $trafficwatch-ids-review para decirme que modulos existen y que hace cada uno.`
- `Usa $trafficwatch-ids-review para comparar el README con el codigo actual.`
- `Usa $trafficwatch-ids-review para comparar FD04 con web/app.py y decir que falta actualizar.`
- `Usa $trafficwatch-ids-review para revisar si el dashboard consume APIs inexistentes.`
- `Usa $trafficwatch-ids-review para resumir el proyecto para una exposicion.`

Si el usuario primero pregunta que puede hacer la skill, explica sus capacidades y luego sugiere prompts concretos. En turnos posteriores, pide o espera que vuelva a mencionar `$trafficwatch-ids-review` para activar la skill de forma explicita.

## Cuando Usarla

Activa esta skill cuando la solicitud mencione o afecte:

- Reglas de deteccion IDS, clasificacion de trafico, falsos positivos o umbrales.
- Alertas, incidentes, historial, exportacion CSV/JSON o agregacion del dashboard.
- Botones del dashboard, JavaScript, estilos, navegacion o consumo de APIs.
- Bloqueo temporal de IP, Firewall de Windows, respuesta activa o modo prueba.
- Red local, escaneo de equipos, laboratorio de 100 equipos, Nmap, Scapy o Suricata.
- Ejecucion local en Windows, empaquetado, instaladores o scripts `.bat`/`.ps1`.
- Despliegue en Render, variables de entorno o limitaciones de hosting.
- Pruebas automatizadas, documentacion academica, README o informes.

## Primer Paso

1. Lee `README.md`, `config.json` y los archivos directamente relacionados con la solicitud.
2. Revisa `tests/` antes de modificar deteccion, almacenamiento, respuesta activa, APIs o dashboard.
3. Verifica si el cambio aplica a ejecucion local, demo Render o ambos.
4. Trata `logs/` como datos de ejecucion. No dependas de logs reales versionados ni los conviertas en fixtures.
5. Antes de tocar red, firewall, instaladores o capturas reales, confirma que el usuario lo pidio explicitamente.

## Mapa Del Proyecto

- `main.py`: arranque local del IDS. Carga configuracion, detecta red, inicia captura y actualiza estado.
- `src/packet_capture.py`: captura de paquetes con Scapy para la ejecucion local del IDS.
- `src/analyzer.py`: reglas IDS para escaneo de puertos, ICMP flood, SYN flood, fuerza bruta, alta frecuencia, puertos sospechosos y puertos raros.
- `src/alert_manager.py`: creacion de alertas, cooldown, categorias, persistencia y metadatos de respuesta.
- `src/storage.py`: lectura/escritura JSON con limite de registros y tolerancia a corrupcion.
- `src/network_utils.py`: deteccion de red en Windows y comandos sugeridos.
- `src/status_manager.py`: estado operativo del IDS, interfaz usada, red detectada y ultimo latido.
- `src/network_scanner.py`: escaneo controlado de red local para inventario del dashboard.
- `src/real_scan.py`: validacion de objetivos y ejecucion controlada de escaneos Nmap locales.
- `src/response_actions.py`: respuesta activa con Firewall de Windows y bloqueo temporal conservador.
- `src/suricata_integration.py`: estado de Suricata, eventos EVE, reglas, planes IPS y comandos sugeridos.
- `run_dashboard.py`: arranque local del dashboard Flask.
- `web/app.py`: rutas Flask, APIs, simulacion, incidentes, exportaciones, red local, Suricata, IPS y Render.
- `web/templates/dashboard.html`: dashboard principal, navegacion, tablas, botones y consumo de APIs.
- `web/templates/attack_lab.html`: laboratorio controlado para simulaciones.
- `suricata/local.rules`: reglas locales de Suricata.
- `config.json`: umbrales, rutas de logs, ventana de incidentes, limites de red, Suricata y respuesta activa.
- `docs/`: documentacion academica, arquitectura, requerimientos, despliegue Render y guia Suricata IPS.
- `tests/`: pruebas de analizador, alertas, almacenamiento, red, APIs y respuesta activa.
- Scripts Windows: `INICIAR_TRAFFICWATCH.bat`, `setup_windows.ps1`, instalador, empaquetado y ayudantes de administrador.
- `render.yaml` y `runtime.txt`: despliegue de demostracion en Render.

## Reglas De Trabajo

- Prefiere cambios pequenos, claros y enfocados.
- Manten umbrales y limites configurables en `config.json`; evita constantes rigidas de seguridad.
- Conserva nombres de alerta consistentes entre analizador, simulador, dashboard, respuesta activa, Suricata y pruebas.
- Agrega o actualiza pruebas cuando cambies reglas IDS, formatos de alerta, respuesta activa, APIs o comportamiento del dashboard.
- Manten separacion estricta:
  - Local Windows: captura real, Scapy, firewall, Suricata, Nmap y escaneo de red.
  - Render: dashboard, simulaciones, historial, graficos y demostraciones seguras.
- No ejecutes escaneos reales, captura de paquetes, Suricata, Nmap, cambios de firewall, instaladores o scripts de administrador salvo solicitud explicita.
- Si una funcion puede bloquear una IP, debe ser manual, visible para el usuario, temporal, reversible y validada.
- Para laboratorios grandes, evita una fila por paquete cuando sea mejor agrupar por incidente, IP, tipo, puerto y ventana temporal.
- Conserva textos en espanol del dashboard y documentacion, salvo que la tarea pida traduccion.
- Para cambios en `docs/`, conserva el tono academico, la estructura FD01-FD06 y la coherencia con README, Render y las funciones reales del sistema.
- No agregues al commit archivos generados, `dist/`, `build/`, `__pycache__/`, logs reales, capturas locales ni rutas especificas de una maquina.

## Seguridad Y Alcance Permitido

Este proyecto es defensivo y academico. Es correcto ayudar con:

- Simulaciones controladas dentro de laboratorio autorizado.
- Deteccion, visualizacion, clasificacion y explicacion de eventos.
- Bloqueo temporal defensivo desde el equipo donde corre el IDS.
- Mejoras de escalabilidad para redes locales autorizadas.
- Validaciones que eviten acciones peligrosas por accidente.

Evita:

- Instrucciones para atacar terceros o evadir defensas.
- Automatizar bloqueos masivos sin confirmacion.
- Ejecutar comandos que cambien firewall/red sin autorizacion explicita.
- Convertir pruebas de laboratorio en herramientas ofensivas reutilizables contra redes externas.

## Flujo Recomendado Por Tipo De Tarea

### Cambios En Deteccion

1. Revisa `src/analyzer.py`, `config.json` y pruebas relacionadas.
2. Verifica que el tipo de alerta exista o se refleje en dashboard/simulador/exportaciones.
3. Cuida cooldown y agrupacion para no generar ruido excesivo.
4. Prueba con casos pequenos y deterministas.

### Cambios En Dashboard

1. Revisa `web/templates/dashboard.html` y los endpoints usados en `web/app.py`.
2. Asegura que el JavaScript soporte campos faltantes o respuestas vacias.
3. Manten actualizacion automatica sin duplicar filas innecesariamente.
4. Verifica renderizado con `app.test_client()` cuando baste.

### Cambios En Respuesta Activa

1. Revisa `src/response_actions.py`, `web/app.py`, `config.json` y pruebas.
2. Manten duracion configurable y por defecto conservadora para laboratorio.
3. Valida IPs, evita rangos peligrosos y registra la accion de forma comprensible.
4. No ejecutes firewall real si solo necesitas probar construccion de comandos.

### Cambios En Red Local

1. Limita el alcance a la red local detectada o configurada.
2. Usa timeouts, cache y limite de hosts/trabajadores.
3. Para laboratorios de hasta 100 equipos, prioriza escaneo acotado, resultados cacheados y reintentos controlados.
4. No dependas de nombres DNS/reverse lookup para que el dashboard funcione.

### Cambios En Render

1. Recuerda que Render no puede capturar trafico real ni modificar firewall local.
2. Usa variables de entorno y rutas portables.
3. Evita depender de Windows, Npcap, Suricata local o permisos de administrador.
4. Manten simulaciones y vistas demo funcionales.

## No Hacer

- No ejecutes capturas reales, escaneos Nmap, Suricata real, cambios de firewall, instaladores o scripts de administrador sin pedido explicito del usuario.
- No uses logs reales como fixtures, datos fuente o evidencia estable.
- No rompas la compatibilidad con Render al agregar funciones que dependan de Windows, red local, permisos de administrador, Nmap, Npcap o Suricata.

## Validacion

Usa la validacion mas especifica posible:

```powershell
python -m json.tool config.json
python -m compileall src web
python -m pytest
```

Pruebas enfocadas utiles:

```powershell
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
python -m pytest tests/test_storage.py
```

Prueba rapida para dashboard/API:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

Si `pytest` no esta instalado, informa el bloqueo y ejecuta al menos:

```powershell
python -m json.tool config.json
python -m compileall src web
```

## Checklist De Revision

Antes de terminar, revisa:

- El cambio rompe `config.json` o introduce claves no documentadas?
- Los tipos de alerta siguen coincidiendo entre backend, frontend, simulador y pruebas?
- El dashboard tolera listas vacias, campos nulos y errores de API?
- La agrupacion de incidentes evita ruido sin ocultar eventos importantes?
- La respuesta activa sigue siendo manual, temporal y reversible?
- Render sigue funcionando aunque no existan herramientas locales de red?
- Las pruebas no dependen de red real, logs reales ni permisos de administrador?
- No se agregaron archivos generados o datos locales al commit?

## Respuesta Al Usuario

Al finalizar una tarea, explica en espanol:

- Que se reviso o cambio.
- Que validacion se ejecuto y su resultado.
- Si aplica, que queda pendiente para probar en Windows, red local o Render.
- Si hubo una decision de seguridad, explicala de forma simple y practica.
