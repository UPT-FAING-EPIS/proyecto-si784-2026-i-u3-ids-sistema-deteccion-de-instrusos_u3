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

# Documento de Vision

Version: **2.0**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-14 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |

## 1. Introduccion

### 1.1 Proposito

Este documento describe la vision del sistema **TrafficWatch IDS**, una herramienta academica para monitoreo de trafico de red y deteccion de comportamientos sospechosos en tiempo real.

El documento sirve como referencia para comprender el problema, los usuarios, el alcance, las capacidades actuales y las restricciones del producto.

### 1.2 Alcance

TrafficWatch IDS esta orientado a redes locales, equipos personales y laboratorios academicos en Windows. El sistema permite capturar trafico, analizar paquetes mediante reglas IDS y visualizar alertas en un dashboard web local.

La version actual incluye:

- Dashboard web.
- Historial de alertas.
- Filtros y paginacion.
- Graficos.
- Exportacion JSON/CSV.
- Estado operativo del IDS.
- Trafico clasificado.
- Scripts de arranque automatico.

No incluye bloqueo automatico ni mitigacion activa.

### 1.3 Definiciones

| Termino | Definicion |
|---|---|
| IDS | Sistema de deteccion de intrusos que alerta sobre actividad sospechosa. |
| IPS | Sistema de prevencion de intrusos que puede bloquear trafico. |
| Scapy | Libreria Python para captura y analisis de paquetes. |
| Flask | Framework web usado para el dashboard. |
| Nmap | Herramienta usada para pruebas autorizadas de escaneo. |
| Gateway | Puerta de enlace de la red local. |
| Alerta | Registro generado por una regla IDS. |

## 2. Posicionamiento

### 2.1 Oportunidad

Muchas redes academicas o pequenas no cuentan con herramientas simples para observar trafico y comprender eventos sospechosos. Las soluciones comerciales pueden ser costosas o complejas para estudiantes.

TrafficWatch IDS ofrece una alternativa gratuita, didactica y ejecutable en Windows para aprender conceptos de IDS, redes y pruebas de software.

### 2.2 Problema

La falta de monitoreo dificulta identificar escaneos de puertos, intentos repetidos de conexion, trafico inusual o accesos hacia puertos sensibles. Esto genera desconocimiento sobre lo que ocurre en la red local.

TrafficWatch IDS aborda este problema capturando paquetes, clasificando trafico y generando alertas interpretables.

## 3. Interesados y usuarios

| Actor | Descripcion | Necesidad |
|---|---|---|
| Estudiante | Usuario principal del sistema. | Ejecutar pruebas y comprender alertas. |
| Desarrollador | Mantiene y mejora el proyecto. | Modificar reglas, dashboard y scripts. |
| Docente | Evalua el proyecto academico. | Ver evidencias, documentacion y resultados. |
| Analista de red principiante | Interpreta trafico local. | Observar eventos y exportar informacion. |

## 4. Vista general del producto

### 4.1 Perspectiva

El producto funciona como una aplicacion local con dos procesos principales:

- **IDS:** captura y analiza paquetes con permisos de administrador.
- **Dashboard:** muestra informacion en `http://127.0.0.1:5000`.

Ambos procesos pueden ejecutarse mediante archivos `.bat`.

### 4.2 Capacidades

| Capacidad | Descripcion |
|---|---|
| Captura de paquetes | Observa trafico en tiempo real con Scapy. |
| Deteccion por reglas | Evalua patrones configurados en `config.json`. |
| Alertas | Guarda eventos en `logs/alerts.json`. |
| Trafico clasificado | Guarda ultimos paquetes en `logs/traffic.json`. |
| Estado IDS | Mantiene informacion en `logs/status.json`. |
| Dashboard | Presenta tablas, historial, graficos y exportaciones. |
| Pruebas guiadas | Genera ejemplos segun red detectada. |

## 5. Caracteristicas del producto

### 5.1 Reglas IDS

La version actual detecta:

- `ESCANEO_DE_PUERTOS`
- `SYN_FLOOD`
- `ICMP_FLOOD`
- `PUERTO_SOSPECHOSO`
- `PUERTO_RARO`
- `ALTA_FRECUENCIA_CONEXIONES`
- `FUERZA_BRUTA_FTP`
- `FUERZA_BRUTA_SSH`
- `FUERZA_BRUTA_TELNET`
- `FUERZA_BRUTA_RDP`

### 5.2 Dashboard

El dashboard incluye:

- Resumen de alertas.
- Tipos de trafico.
- Trafico clasificado.
- Estado IDS.
- Graficos.
- Historial con filtros.
- Reglas IDS.

### 5.3 Automatizacion

Archivos principales:

- `setup_windows.ps1`
- `abrir_cmd_proyecto.bat`
- `abrir_powershell_admin.bat`
- `abrir_powershell_pruebas.bat`
- `simular_fuerza_bruta.py`

## 6. Restricciones

- El IDS principal requiere permisos de administrador.
- Nmap debe estar instalado para pruebas de escaneo.
- El sistema esta enfocado en Windows.
- El dashboard es local y no tiene autenticacion.
- El sistema detecta y alerta, pero no bloquea.
- Debe usarse solo en redes autorizadas.

## 7. Calidad esperada

| Atributo | Descripcion |
|---|---|
| Usabilidad | Uso simplificado mediante `.bat` y dashboard. |
| Mantenibilidad | Codigo modular separado por captura, analisis, alertas, storage y web. |
| Auditabilidad | Logs en JSON y exportacion CSV. |
| Configurabilidad | Reglas y umbrales en `config.json`. |
| Portabilidad limitada | Enfoque actual en Windows. |

## 8. Conclusion

TrafficWatch IDS cumple la vision de una herramienta academica para monitoreo y deteccion basica de intrusiones. La version actual es mas completa que el prototipo inicial, ya que incorpora dashboard avanzado, graficos, exportaciones, clasificacion de trafico, estado operativo y reglas IDS ampliadas.
