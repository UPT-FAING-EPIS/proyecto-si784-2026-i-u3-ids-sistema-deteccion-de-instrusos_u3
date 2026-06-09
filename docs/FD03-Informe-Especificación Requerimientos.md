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

# Informe de Especificacion de Requerimientos

Version: **2.0**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-20 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |

## 1. Introduccion

Este documento especifica los requerimientos funcionales y no funcionales de **TrafficWatch IDS**, sistema de deteccion de intrusos para monitoreo de trafico de red en Windows.

## 2. Alcance funcional

El sistema permite:

- Capturar paquetes de red.
- Analizar trafico con reglas IDS.
- Generar alertas.
- Guardar historial.
- Clasificar trafico.
- Mostrar dashboard web.
- Exportar informacion.
- Ejecutar pruebas guiadas.

El sistema no bloquea trafico ni reemplaza herramientas empresariales de seguridad.

## 3. Requerimientos funcionales

| ID | Requerimiento | Prioridad | Evidencia |
|---|---|---|---|
| RF-01 | Capturar paquetes de red en tiempo real. | Alta | `main.py`, `src/packet_capture.py` |
| RF-02 | Detectar escaneo de puertos. | Alta | Regla `port_scan` en `config.json` |
| RF-03 | Detectar SYN flood. | Alta | Regla `syn_flood` |
| RF-04 | Detectar ICMP flood. | Media | Regla `icmp_flood` |
| RF-05 | Detectar fuerza bruta hacia FTP, SSH, Telnet y RDP. | Alta | Regla `brute_force` |
| RF-06 | Detectar alta frecuencia de conexiones. | Media | Regla `connection_frequency` |
| RF-07 | Detectar puertos sospechosos. | Media | Regla `suspicious_ports` |
| RF-08 | Detectar puertos raros configurados. | Media | Regla `rare_ports` |
| RF-09 | Aplicar cooldown para alertas repetidas. | Alta | `src/alert_manager.py` |
| RF-10 | Guardar alertas en JSON. | Alta | `logs/alerts.json` |
| RF-11 | Clasificar trafico observado. | Media | `logs/traffic.json` |
| RF-12 | Mostrar dashboard web local. | Alta | `web/app.py`, `dashboard.html` |
| RF-13 | Filtrar y paginar historial. | Media | Seccion Historial |
| RF-14 | Exportar alertas en JSON y CSV. | Media | `/api/export/alerts.*` |
| RF-15 | Exportar trafico clasificado en JSON y CSV. | Media | `/api/export/traffic.*` |
| RF-16 | Mostrar estado del IDS. | Media | `/api/status`, `logs/status.json` |
| RF-17 | Mostrar graficos de alertas. | Media | `/api/charts` |
| RF-18 | Generar ejemplos de pruebas segun la red detectada. | Media | `src/network_utils.py` |
| RF-19 | Automatizar arranque con scripts Windows. | Alta | Archivos `.bat` y `.ps1` |

## 4. Requerimientos no funcionales

| ID | Requerimiento | Criterio |
|---|---|---|
| RNF-01 | Usabilidad | El usuario puede iniciar dashboard, IDS y pruebas mediante `.bat`. |
| RNF-02 | Rendimiento | El IDS procesa trafico moderado de laboratorio en tiempo real. |
| RNF-03 | Mantenibilidad | El codigo se organiza en modulos separados. |
| RNF-04 | Configurabilidad | Reglas y umbrales se definen en `config.json`. |
| RNF-05 | Auditabilidad | Alertas y trafico quedan en JSON y pueden exportarse. |
| RNF-06 | Seguridad de uso | El sistema documenta que debe ejecutarse solo en redes autorizadas. |
| RNF-07 | Compatibilidad | Enfoque principal en Windows. |
| RNF-08 | Disponibilidad local | Dashboard disponible en `http://127.0.0.1:5000` cuando `run_dashboard.py` esta activo. |

## 5. Reglas de negocio IDS

| Regla | Descripcion |
|---|---|
| ESCANEO_DE_PUERTOS | Una IP accede a varios puertos distintos en una ventana corta. |
| SYN_FLOOD | Exceso de paquetes TCP SYN desde una misma IP. |
| ICMP_FLOOD | Exceso de paquetes ICMP desde una misma IP. |
| FUERZA_BRUTA_* | Intentos repetidos hacia servicios comunes. |
| ALTA_FRECUENCIA_CONEXIONES | Muchas conexiones TCP desde una misma IP aunque no sean a muchos puertos. |
| PUERTO_SOSPECHOSO | Conexion hacia puertos sensibles configurados. |
| PUERTO_RARO | Conexion hacia puertos poco comunes configurados. |

## 6. Casos de uso

| Caso | Actor | Flujo principal |
|---|---|---|
| CU-01 Iniciar dashboard | Usuario | Ejecuta `abrir_cmd_proyecto.bat` y abre localhost. |
| CU-02 Iniciar IDS | Usuario | Ejecuta `abrir_powershell_admin.bat`, acepta permisos y deja capturando. |
| CU-03 Ejecutar pruebas | Usuario | Abre `abrir_powershell_pruebas.bat` y ejecuta ejemplos sugeridos. |
| CU-04 Consultar alertas | Usuario | Revisa dashboard e historial. |
| CU-05 Exportar informacion | Usuario | Descarga JSON o CSV de alertas/trafico. |
| CU-06 Revisar estado IDS | Usuario | Entra a seccion Estado IDS. |
| CU-07 Analizar graficos | Usuario | Entra a seccion Graficos. |

## 7. Interfaces

### 7.1 Interfaz web

Secciones implementadas:

- Dashboard.
- Tipos de trafico.
- Trafico clasificado.
- Estado IDS.
- Graficos.
- Historial.
- Reglas IDS.

### 7.2 API local Flask

| Ruta | Funcion |
|---|---|
| `/api/alerts` | Lista alertas. |
| `/api/traffic` | Lista trafico clasificado. |
| `/api/status` | Devuelve estado del IDS. |
| `/api/charts` | Devuelve datos para graficos. |
| `/api/clear` | Borra historial de alertas. |
| `/api/export/alerts.json` | Exporta alertas JSON. |
| `/api/export/alerts.csv` | Exporta alertas CSV. |
| `/api/export/traffic.json` | Exporta trafico JSON. |
| `/api/export/traffic.csv` | Exporta trafico CSV. |

## 8. Criterios de aceptacion

- El dashboard abre en `http://127.0.0.1:5000`.
- El IDS captura paquetes al ejecutarse como administrador.
- Las pruebas de Nmap generan alertas de escaneo cuando superan el umbral.
- `simular_fuerza_bruta.py` genera alertas de fuerza bruta cuando alcanza el umbral.
- El historial permite filtrar, paginar y borrar alertas.
- Los graficos se actualizan con el historial.
- Los archivos JSON/CSV se descargan correctamente.

## 9. Conclusiones

Los requerimientos actuales reflejan una version funcional del IDS academico. El proyecto evoluciono desde una captura basica con alertas hacia una herramienta con dashboard completo, reglas ampliadas, estado operativo, clasificacion de trafico, graficos, exportaciones y automatizacion para Windows.
