![Logo](../media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingenieria de Sistemas**

**Proyecto TrafficWatch IDS**

Curso: **Calidad y Pruebas de Software**

Docente: **MAG. Patrick Cuadros Quiroga**

Integrantes:

- **Edgar Diego Chara Apaza (2019065026)**
- **Abel Fernando Pacompia Ortiz (2023076797)**

**Tacna - Peru**

**2026**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# Informe de Arquitectura de Software

Version: **2.3**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-25 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |
| 2.1 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-07-04 | Actualizacion segun dashboard, Suricata IPS, respuesta activa y despliegue Render |
| 2.2 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-07-04 | Revision de coherencia con informes FD01-FD05 y codigo actual |
| 2.3 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-07-04 | Se agregan vistas de casos de uso, subsistemas y secuencia de diseno |

## 1. Introduccion

Este documento describe la arquitectura de **TrafficWatch IDS**, sistema de deteccion de intrusos construido con Python, Scapy y Flask para ejecucion local en Windows y demostracion web en Render.

La arquitectura separa el proceso local de captura/analisis del proceso web de visualizacion. Ambos comparten archivos JSON como mecanismo simple de persistencia. El dashboard tambien incorpora simulaciones, escaneo local controlado, integracion con Suricata EVE, politicas IPS y respuesta activa manual para escenarios autorizados.

## 2. Vista general

```mermaid
flowchart LR
    USER[Usuario] --> BAT[Scripts .bat/.ps1]
    BAT --> IDS[Proceso IDS main.py]
    BAT --> WEB[Dashboard Flask]
    IDS --> SCAPY[Scapy]
    SCAPY --> ANALYZER[TrafficAnalyzer]
    ANALYZER --> ALERTS[logs/alerts.json]
    ANALYZER --> TRAFFIC[logs/traffic.json]
    IDS --> STATUS[logs/status.json]
    WEB --> ALERTS
    WEB --> TRAFFIC
    WEB --> STATUS
    WEB --> POLICIES[logs/policies.json]
    WEB --> SURIEVENTS[logs/suricata/eve.json]
    WEB --> NMAP[Nmap local controlado]
    WEB --> SCANNER[Escaneo de red local]
    WEB --> FIREWALL[Windows Firewall manual]
    WEB --> UI[Dashboard HTML]
    WEB --> ATTACKLAB[Attack Lab]
```

## 3. Representacion de la arquitectura del sistema

Esta seccion representa la arquitectura desde diferentes vistas para relacionar actores, funcionalidades, subsistemas y colaboraciones internas del aplicativo.

### 3.1 Vista de caso de uso

La vista de caso de uso muestra como interactuan los usuarios con TrafficWatch IDS. El usuario principal administra el dashboard, revisa alertas y ejecuta pruebas controladas. El administrador del sistema puede iniciar la captura real y aplicar acciones defensivas autorizadas. Render actua como entorno externo de demostracion web.

```mermaid
flowchart LR
    USR[Usuario del sistema]
    ADM[Administrador]
    REM[Usuario remoto autorizado]
    RENDER[Render]

    subgraph APP[TrafficWatch IDS]
        UC1[Iniciar dashboard]
        UC2[Consultar alertas e incidentes]
        UC3[Exportar evidencias JSON/CSV]
        UC4[Ejecutar pruebas controladas]
        UC5[Iniciar captura IDS]
        UC6[Escanear red local autorizada]
        UC7[Consultar Suricata IPS]
        UC8[Generar politicas IPS]
        UC9[Aplicar bloqueo SSH temporal]
        UC10[Usar Attack Lab]
        UC11[Ver demo web]
    end

    USR --> UC1
    USR --> UC2
    USR --> UC3
    USR --> UC4
    USR --> UC6
    USR --> UC7
    USR --> UC8
    ADM --> UC5
    ADM --> UC9
    REM --> UC10
    RENDER --> UC11
```

### 3.1.1 Diagramas de casos de uso

El siguiente diagrama detalla los casos de uso principales y sus relaciones funcionales. Las consultas del dashboard dependen de los logs JSON generados por el IDS o por las simulaciones controladas.

```mermaid
flowchart TD
    ACT[Usuario / Administrador]

    subgraph DASH[Dashboard web]
        A[Abrir dashboard]
        B[Consultar historial]
        C[Ver graficos]
        D[Exportar alertas]
        E[Limpiar historial]
    end

    subgraph IDS[Monitoreo IDS]
        F[Iniciar IDS]
        G[Capturar paquetes]
        H[Analizar trafico]
        I[Generar alertas]
    end

    subgraph LAB[Laboratorio y respuesta]
        J[Ejecutar simulacion]
        K[Usar Attack Lab remoto]
        L[Ejecutar Nmap validado]
        M[Consultar Suricata]
        N[Generar politica IPS]
        O[Bloquear IP SSH temporal]
    end

    ACT --> A
    ACT --> F
    ACT --> J
    ACT --> K
    ACT --> L
    ACT --> M
    ACT --> N
    ACT --> O
    A --> B
    A --> C
    A --> D
    A --> E
    F --> G
    G --> H
    H --> I
    I --> B
    J --> I
    K --> I
    L --> I
    M --> B
    N --> B
```

### 3.2 Vista de diseno

La vista de diseno describe la organizacion interna del aplicativo mediante subsistemas y la colaboracion entre componentes durante un flujo de deteccion.

### 3.2.1 Diagrama de subsistemas (paquetes)

La arquitectura se divide en paquetes funcionales. Cada paquete agrupa responsabilidades especificas y reduce el acoplamiento entre la captura, el analisis, la interfaz, la persistencia y las integraciones externas.

```mermaid
flowchart LR
    subgraph UI[web]
        WEBAPP[app.py]
        TPL[templates]
    end

    subgraph CORE[src]
        CAP[packet_capture.py]
        ANA[analyzer.py]
        ALERT[alert_manager.py]
        STATUS[status_manager.py]
        STORE[storage.py]
        NET[network_utils.py]
    end

    subgraph INTEG[Integraciones]
        SCAN[network_scanner.py]
        NMAP[real_scan.py]
        RESP[response_actions.py]
        SURI[suricata_integration.py]
    end

    subgraph DATA[Datos y configuracion]
        CFG[config.json]
        LOGS[logs/*.json]
        RULES[suricata/local.rules]
    end

    subgraph DEPLOY[Despliegue y calidad]
        RENDER[render.yaml]
        WF[.github/workflows]
        DOCS[docs]
    end

    WEBAPP --> STORE
    WEBAPP --> SCAN
    WEBAPP --> NMAP
    WEBAPP --> RESP
    WEBAPP --> SURI
    TPL --> WEBAPP
    CAP --> ANA
    ANA --> ALERT
    ANA --> STORE
    ALERT --> RESP
    STATUS --> STORE
    CORE --> CFG
    STORE --> LOGS
    SURI --> RULES
    DEPLOY --> WEBAPP
```

### 3.2.2 Diagrama de secuencia (vista de diseno)

La vista de diseno representa la colaboracion interna cuando el sistema detecta trafico sospechoso y actualiza el dashboard.

```mermaid
sequenceDiagram
    actor Usuario
    participant Dashboard as Dashboard Flask
    participant IDS as main.py
    participant Captura as PacketCapture
    participant Analizador as TrafficAnalyzer
    participant Alertas as AlertManager
    participant Respuesta as ActiveResponse
    participant Logs as Storage JSON

    Usuario->>Dashboard: Abre dashboard local
    Usuario->>IDS: Inicia captura como administrador
    IDS->>Captura: Configura interfaz de red
    Captura->>Analizador: Envia paquete capturado
    Analizador->>Analizador: Clasifica trafico y evalua reglas
    Analizador->>Logs: Guarda trafico clasificado
    Analizador->>Alertas: Solicita generar alerta
    Alertas->>Alertas: Valida cooldown
    Alertas->>Respuesta: Obtiene recomendacion defensiva
    Respuesta-->>Alertas: Devuelve accion sugerida
    Alertas->>Logs: Guarda alerta
    Dashboard->>Logs: Consulta alertas, trafico y estado
    Logs-->>Dashboard: Devuelve datos JSON
    Dashboard-->>Usuario: Presenta historial, graficos y acciones
```

## 4. Componentes

| Componente | Archivo | Responsabilidad |
|---|---|---|
| Programa principal | `main.py` | Carga configuracion, detecta red, inicia captura y estado IDS. |
| Captura | `src/packet_capture.py` | Captura paquetes con Scapy. |
| Analizador | `src/analyzer.py` | Clasifica trafico y aplica reglas IDS. |
| Alertas | `src/alert_manager.py` | Genera alertas y aplica cooldown. |
| Persistencia | `src/storage.py` | Lee, guarda y limpia archivos JSON. |
| Red | `src/network_utils.py` | Detecta IP, gateway, red y genera ejemplos de prueba. |
| Estado | `src/status_manager.py` | Escribe estado operativo del IDS. |
| Escaneo de red | `src/network_scanner.py` | Detecta dispositivos activos de la red local con ping sweep y tabla ARP. |
| Escaneo Nmap | `src/real_scan.py` | Ejecuta Nmap local con objetivo validado y rangos de puertos permitidos. |
| Respuesta activa | `src/response_actions.py` | Genera recomendaciones y aplica bloqueo temporal de IP cuando se solicita con permisos. |
| Suricata IPS | `src/suricata_integration.py` | Lee EVE JSON, genera eventos demo, comandos firewall, reglas drop y planes IPS inline. |
| Dashboard | `web/app.py` | Expone rutas Flask y APIs locales. |
| Interfaz | `web/templates/dashboard.html` | Renderiza dashboard, tablas, graficos y acciones. |
| Laboratorio web | `web/templates/attack_lab.html` | Permite trafico remoto controlado y pruebas autorizadas. |
| Simulador | `simular_fuerza_bruta.py` | Genera conexiones TCP repetidas para laboratorio. |
| Configuracion | `config.json` | Centraliza interfaz, reglas IDS, logs, dashboard, Suricata, escaneo y respuesta activa. |
| Despliegue Render | `render.yaml`, `runtime.txt` | Publican el dashboard de demostracion sin captura real ni firewall local. |

## 5. Vista de procesos

### 5.1 Arranque recomendado

```mermaid
flowchart TD
    A[abrir_cmd_proyecto.bat] --> B[python run_dashboard.py]
    B --> C[Dashboard en localhost:5000]
    D[abrir_powershell_admin.bat] --> E[Solicita permisos admin]
    E --> F[python main.py]
    F --> G[Captura paquetes]
    H[abrir_powershell_pruebas.bat] --> I[Muestra ejemplos segun red]
    I --> J[Usuario ejecuta pruebas]
    J --> G
    K[CREAR_EJECUTABLE_WINDOWS.bat] --> L[PyInstaller]
    M[Render] --> N[Dashboard demo sin captura real]
```

### 5.2 Flujo de deteccion

```mermaid
sequenceDiagram
    participant Red as Red local
    participant Cap as PacketCapture
    participant Ana as TrafficAnalyzer
    participant Alert as AlertManager
    participant Resp as ActiveResponse
    participant Log as Logs JSON
    participant Web as Dashboard

    Red->>Cap: Paquete observado
    Cap->>Ana: Envia paquete
    Ana->>Ana: Clasifica trafico
    Ana->>Log: Guarda trafico clasificado
    Ana->>Ana: Evalua reglas IDS
    Ana->>Alert: Solicita alerta
    Alert->>Alert: Verifica cooldown
    Alert->>Resp: Adjunta respuesta recomendada si aplica
    Alert->>Log: Guarda alerta
    Web->>Log: Consulta APIs
    Web->>Web: Actualiza tablas y graficos
```

## 6. Vista logica

```mermaid
classDiagram
    class PacketCapture {
        +interface
        +packet_callback
        +start()
    }

    class TrafficAnalyzer {
        +rules
        +analyze_packet(packet)
        -_analyze_tcp(packet, source, destination)
        -_analyze_icmp(source)
        -_record_traffic(packet, source, destination)
        -_classify_traffic(source, destination)
    }

    class AlertManager {
        +cooldown_seconds
        +active_response
        +generate_alert(level, type, source_ip, description)
    }

    class AlertStorage {
        +save(record)
        +read()
        +clear()
    }

    class StatusManager {
        +start(interface, network_info)
        +heartbeat()
        +stop()
        -_write()
    }

    class FlaskDashboard {
        +api_alerts()
        +api_incidents()
        +api_traffic()
        +api_status()
        +api_charts()
        +api_network_devices()
        +api_real_nmap_scan()
        +api_suricata_status()
        +api_ips_policies()
        +export_alerts()
        +export_traffic()
    }

    class ActiveResponse {
        +build_response(alert_type, source_ip)
        +block_ip_temporarily(source_ip)
    }

    class SuricataIntegration {
        +read_suricata_alerts()
        +get_suricata_status()
        +build_firewall_block_command()
        +build_inline_ips_plan()
    }

    class NetworkScanner {
        +scan_local_network()
    }

    PacketCapture --> TrafficAnalyzer
    TrafficAnalyzer --> AlertManager
    TrafficAnalyzer --> AlertStorage
    AlertManager --> AlertStorage
    AlertManager --> ActiveResponse
    FlaskDashboard --> AlertStorage
    FlaskDashboard --> NetworkScanner
    FlaskDashboard --> SuricataIntegration
    FlaskDashboard --> ActiveResponse
```

## 7. Vista de datos

El sistema usa persistencia en archivos JSON:

| Archivo | Contenido |
|---|---|
| `logs/alerts.json` | Historial de alertas IDS. |
| `logs/traffic.json` | Ultimos paquetes clasificados. |
| `logs/status.json` | Estado operativo del IDS. |
| `logs/policies.json` | Politicas IPS generadas desde el dashboard. |
| `logs/suricata/eve.json` | Eventos Suricata EVE reales o de demostracion. |
| `suricata/local.rules` | Reglas locales Suricata utilizadas como referencia IPS. |
| `config.json` | Configuracion de reglas IDS, dashboard, escaneo, Suricata y respuesta activa. |

Las alertas y el trafico clasificado tambien pueden exportarse a JSON y CSV desde el dashboard.

## 8. Vista web/API

| Ruta | Descripcion |
|---|---|
| `/` | Dashboard principal. |
| `/attack-lab` | Laboratorio web de trafico controlado. |
| `/api/alerts` | Alertas. |
| `/api/incidents` | Alertas agrupadas como incidentes activos. |
| `/api/traffic` | Trafico clasificado. |
| `/api/status` | Estado IDS. |
| `/api/charts` | Datos para graficos. |
| `/api/stats` | Resumen estadistico de alertas. |
| `/api/network/devices` | Escaneo controlado de dispositivos de la red local. |
| `/api/real-scan/nmap` | Escaneo Nmap local validado. |
| `/api/suricata/status` | Estado de eve.json y reglas Suricata. |
| `/api/suricata/alerts` | Alertas normalizadas desde Suricata EVE. |
| `/api/suricata/demo-alert` | Genera un evento EVE de demostracion. |
| `/api/ips/block-command` | Construye comandos de bloqueo para firewall o Suricata. |
| `/api/ips/inline-plan` | Genera plan de laboratorio IPS inline con NFQUEUE. |
| `/api/ips/youtube-policy` | Devuelve politica sugerida para YouTube. |
| `/api/ips/youtube-block-command` | Genera reglas Suricata para restringir YouTube por IP. |
| `/api/ips/youtube-policy/save` | Guarda una politica IPS generada. |
| `/api/ips/policies` | Lista politicas IPS guardadas. |
| `/api/firewall/block-ssh-ip` | Aplica bloqueo temporal SSH si existe alerta valida y permisos. |
| `/api/simulate/<attack_type>` | Genera alertas locales simuladas. |
| `/api/remote-attack/<attack_type>` | Registra ataque remoto simulado. |
| `/api/remote-lab-traffic/<traffic_type>` | Registra trafico remoto controlado desde Attack Lab. |
| `/api/clear` | Borrar historial. |
| `/api/export/alerts.json` | Exportar alertas JSON. |
| `/api/export/alerts.csv` | Exportar alertas CSV. |
| `/api/export/traffic.json` | Exportar trafico JSON. |
| `/api/export/traffic.csv` | Exportar trafico CSV. |

## 9. Despliegue

```mermaid
flowchart TD
    PC[PC Windows del usuario]
    PC --> PY[Python]
    PC --> NMAP[Nmap]
    PC --> NPCAP[Npcap/Scapy]
    PY --> IDS[main.py como administrador]
    PY --> WEB[run_dashboard.py sin administrador]
    IDS --> LOGS[Carpeta logs]
    WEB --> LOGS
    WEB --> Browser[Navegador en 127.0.0.1:5000]
    WEB --> LAB[attack-lab]
    WEB --> SURICATA[Suricata local opcional]
    WEB --> FW[Windows Firewall bajo accion manual]
    RENDER[Render] --> WEBDEMO[Dashboard demo]
    WEBDEMO --> DEMOLOGS[Simulaciones e historial demo]
```

La ejecucion local permite captura de paquetes, escaneo de red, Nmap, Suricata local y bloqueo temporal del firewall si existen permisos. La ejecucion en Render es solo demostrativa: muestra dashboard, simulaciones, historial, graficos y laboratorio remoto, pero no captura paquetes locales, no ejecuta Nmap real, no modifica Windows Firewall y no opera Suricata real en la red del usuario.

## 10. Atributos de calidad

| Atributo | Decisiones arquitectonicas |
|---|---|
| Usabilidad | Scripts `.bat`, dashboard web y ejemplos automaticos. |
| Mantenibilidad | Separacion por modulos. |
| Auditabilidad | JSON y CSV exportable, historial de alertas, trafico clasificado y politicas IPS. |
| Rendimiento | Limite de trafico clasificado, cooldown de alertas, cache de escaneo de red y ventanas temporales configurables. |
| Seguridad | Ejecucion local controlada, confirmacion manual de bloqueo, validacion de IPs/rangos y recomendacion de redes autorizadas. |
| Configurabilidad | `config.json` centraliza reglas, umbrales, rutas de logs, escaneo, Suricata, dashboard y respuesta activa. |
| Portabilidad | Dashboard compatible con Windows local, ejecutable empaquetado y demostracion web en Render con funciones locales deshabilitadas o simuladas. |

## 11. Conclusiones

La arquitectura actual es adecuada para un IDS academico con ejecucion local y demostracion web. La separacion entre captura, analisis, almacenamiento, dashboard, Attack Lab, Suricata IPS y respuesta activa permite evolucionar el sistema sin modificar todos los componentes a la vez. La solucion mantiene un alcance controlado: las funciones de captura, Nmap, Suricata real y firewall dependen del entorno local autorizado, mientras que Render se limita a visualizacion, simulaciones, graficos e historial demostrativo.
