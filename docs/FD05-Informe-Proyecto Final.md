![Logo](../media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingenieria de Sistemas**

# Informe Final

## Proyecto TrafficWatch IDS

Curso: **Calidad y Pruebas de Software**

Docente: **MAG. Patrick Cuadros Quiroga**

Integrantes:

- **Edgar Diego Chara Apaza (2019065026)**
- **Abel Fernando Pacompia Ortiz (2023076797)**

**Tacna - Peru**

**2026**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# Control de versiones

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-05-01 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |

## 1. Antecedentes

TrafficWatch IDS surge como proyecto academico para aplicar conocimientos de redes, ciberseguridad, desarrollo de software y pruebas. El sistema permite monitorear trafico de red en tiempo real y generar alertas ante comportamientos sospechosos.

Durante el desarrollo, el proyecto evoluciono desde un prototipo de captura y alertas hacia una herramienta mas completa con dashboard, reglas configurables, historial, graficos, exportacion de evidencias y automatizacion para Windows.

## 2. Planteamiento del problema

Muchas redes locales no cuentan con mecanismos simples para observar trafico y detectar patrones sospechosos. En entornos academicos, ademas, las herramientas comerciales pueden ser costosas o complejas.

TrafficWatch IDS atiende esta necesidad ofreciendo una herramienta local y gratuita para:

- Capturar paquetes.
- Detectar actividad sospechosa.
- Mostrar alertas.
- Registrar evidencias.
- Facilitar pruebas de laboratorio.

## 3. Objetivos

### 3.1 Objetivo general

Desarrollar un sistema basico de deteccion de intrusos capaz de monitorear trafico de red en tiempo real y generar alertas ante actividades sospechosas.

### 3.2 Objetivos especificos

- Implementar captura de paquetes con Scapy.
- Crear reglas IDS configurables.
- Detectar escaneo de puertos, floods, fuerza bruta, alta frecuencia y puertos inusuales.
- Guardar alertas y trafico clasificado en archivos JSON.
- Implementar dashboard web con Flask.
- Agregar historial, filtros, paginacion, graficos y exportaciones.
- Automatizar instalacion y arranque en Windows.
- Documentar uso, pruebas y alcance etico.

## 4. Marco teorico

### 4.1 IDS

Un IDS detecta actividades sospechosas y genera alertas. No bloquea trafico automaticamente. TrafficWatch IDS pertenece a esta categoria.

### 4.2 Reglas de deteccion

El sistema usa reglas basadas en umbrales, frecuencia, puertos y banderas TCP. Estas reglas permiten identificar patrones como escaneo de puertos, fuerza bruta o alto volumen de conexiones.

### 4.3 Herramientas

| Herramienta | Uso |
|---|---|
| Python | Desarrollo principal. |
| Scapy | Captura y analisis de paquetes. |
| Flask | Dashboard web local. |
| Nmap | Pruebas autorizadas de escaneo. |
| PowerShell/CMD | Automatizacion en Windows. |

## 5. Desarrollo de la solucion

### 5.1 Modulos implementados

| Modulo | Descripcion |
|---|---|
| `main.py` | Arranque del IDS, red, captura y estado. |
| `src/packet_capture.py` | Captura de paquetes. |
| `src/analyzer.py` | Analisis, clasificacion y reglas IDS. |
| `src/alert_manager.py` | Alertas con cooldown. |
| `src/storage.py` | Persistencia JSON. |
| `src/network_utils.py` | Deteccion de red y ejemplos. |
| `src/status_manager.py` | Estado operativo del IDS. |
| `web/app.py` | API Flask y exportaciones. |
| `dashboard.html` | Interfaz web. |
| `simular_fuerza_bruta.py` | Simulador de conexiones repetidas. |

### 5.2 Reglas IDS implementadas

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

### 5.3 Dashboard

El dashboard incluye:

- Dashboard principal de alertas.
- Tipos de trafico.
- Trafico clasificado.
- Estado IDS.
- Graficos.
- Historial con filtros y paginacion.
- Reglas IDS.

### 5.4 Automatizacion

Se implementaron scripts para facilitar el uso en Windows:

- `setup_windows.ps1`
- `abrir_cmd_proyecto.bat`
- `abrir_powershell_admin.bat`
- `abrir_powershell_pruebas.bat`

Orden recomendado:

1. Ejecutar `abrir_cmd_proyecto.bat`.
2. Ejecutar `abrir_powershell_admin.bat` y aceptar permisos.
3. Ejecutar `abrir_powershell_pruebas.bat`.

## 6. Pruebas realizadas

| Prueba | Herramienta | Resultado esperado |
|---|---|---|
| Setup Windows | `setup_windows.ps1` | Verifica dependencias y Nmap. |
| Dashboard | `python run_dashboard.py` | Abre localhost. |
| IDS | `python main.py` como admin | Captura paquetes. |
| Escaneo | `nmap -p 1-100 <gateway>` | Genera `ESCANEO_DE_PUERTOS`. |
| Fuerza bruta | `simular_fuerza_bruta.py --port 21 --count 10` | Genera `FUERZA_BRUTA_FTP`. |
| Alta frecuencia | `simular_fuerza_bruta.py --port 80 --count 120 --delay 0.01` | Genera `ALTA_FRECUENCIA_CONEXIONES`. |
| Puerto raro | `nmap -p 31337 <gateway>` | Genera `PUERTO_RARO`. |
| Exportacion | Botones del dashboard | Descarga JSON/CSV. |

## 7. Resultados

El sistema cumple con los objetivos definidos. Permite observar trafico, generar alertas, consultar historial, analizar graficos, exportar evidencias y verificar el estado del IDS.

Los archivos principales de salida son:

- `logs/alerts.json`
- `logs/traffic.json`
- `logs/status.json`

## 8. Presupuesto

| Concepto | Costo estimado |
|---|---:|
| Herramientas de software | S/. 0.00 |
| Equipo propio | S/. 0.00 |
| Internet y energia | S/. 130.00 |
| Materiales y documentacion | S/. 275.00 |
| Tiempo de desarrollo academico | S/. 1600.00 |
| **Total** | **S/. 2005.00** |

## 9. Conclusiones

1. TrafficWatch IDS cumple el objetivo de monitorear trafico de red y generar alertas ante patrones sospechosos.
2. El sistema implementa reglas IDS variadas y configurables, superando el alcance inicial de deteccion basica.
3. El dashboard facilita la interpretacion mediante tablas, historial, filtros, graficos, estado IDS y exportaciones.
4. La automatizacion con `.bat` y `.ps1` mejora la usabilidad en Windows.
5. El sistema mantiene claramente su alcance como IDS: detecta y alerta, pero no bloquea.
6. La solucion es viable para fines academicos, laboratorios y redes autorizadas.

## 10. Recomendaciones

- Agregar autenticacion si el dashboard se expone fuera de localhost.
- Evaluar una base de datos como SQLite si el historial crece mucho.
- Agregar mas pruebas automatizadas para reglas IDS.
- Mantener documentado el uso etico del sistema.
- Separar futuras mejoras IPS en una version distinta para no confundir el alcance.

## 11. Bibliografia

- Sommerville, I. (2016). *Software Engineering*.
- Pressman, R. S., & Maxim, B. R. (2020). *Software Engineering: A Practitioner's Approach*.
- Stallings, W. (2017). *Network Security Essentials*.
- Scarfone, K., & Mell, P. (2007). *Guide to Intrusion Detection and Prevention Systems*. NIST.

## 12. Webgrafia

- Python Documentation: https://docs.python.org/3/
- Scapy Documentation: https://scapy.readthedocs.io/
- Flask Documentation: https://flask.palletsprojects.com/
- Nmap Windows Download: https://nmap.org/download.html#windows
- NIST SP 800-94: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf

## 13. Anexos

- FD01: Informe de Factibilidad.
- FD02: Documento de Vision.
- FD03: Especificacion de Requerimientos.
- FD04: Arquitectura de Software.
- README del proyecto.
- Archivos de configuracion y scripts de ejecucion.
