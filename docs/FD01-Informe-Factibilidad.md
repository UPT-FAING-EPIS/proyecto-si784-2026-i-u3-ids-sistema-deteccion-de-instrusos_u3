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

# Informe de Factibilidad

Version: **2.0**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-05 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |

## 1. Descripcion del proyecto

**TrafficWatch IDS** es un sistema basico de deteccion de intrusos orientado al monitoreo de trafico de red en Windows. El sistema captura paquetes con **Scapy**, analiza el trafico mediante reglas configurables y genera alertas visibles en un dashboard web construido con **Flask**.

El proyecto se ejecuta en un entorno local o de laboratorio. Su objetivo es apoyar el aprendizaje de redes, ciberseguridad y pruebas de software mediante una herramienta accesible y funcional.

## 2. Alcance actual

La version actual incluye:

- Captura de paquetes en tiempo real.
- Deteccion automatica de interfaz, IP local, gateway y red.
- Reglas IDS para escaneo de puertos, SYN flood, ICMP flood, fuerza bruta, alta frecuencia de conexiones, puertos sospechosos y puertos raros.
- Cooldown de alertas repetidas para reducir ruido.
- Clasificacion de trafico entrante, saliente, local, gateway y externo.
- Dashboard web con secciones de alertas, historial, graficos, estado del IDS, trafico clasificado y reglas IDS.
- Exportacion de alertas en JSON/CSV.
- Exportacion de trafico clasificado en JSON/CSV.
- Scripts de automatizacion para Windows.

Fuera de alcance:

- Bloqueo automatico de trafico.
- Integracion con firewall.
- Mitigacion activa de ataques.
- Operacion como IDS empresarial de alta demanda.

Por ello, el sistema debe considerarse un **IDS**, no un **IPS**.

## 3. Riesgos

| Riesgo | Descripcion | Mitigacion |
|---|---|---|
| Falsos positivos | Trafico legitimo puede activar alertas. | Uso de cooldown, umbrales configurables y pruebas controladas. |
| Permisos insuficientes | Scapy requiere permisos de administrador para capturar paquetes. | Uso de `abrir_powershell_admin.bat`. |
| Dependencia de Nmap | Las pruebas de escaneo requieren Nmap instalado. | `setup_windows.ps1` verifica e intenta instalar Nmap con winget. |
| Ruido en red | Muchas conexiones normales pueden generar registros. | Limite de registros de trafico y reglas diferenciadas. |
| Uso indebido | El sistema podria usarse fuera de redes autorizadas. | Documentacion de uso etico y enfoque academico. |

## 4. Factibilidad tecnica

El proyecto es tecnicamente viable porque utiliza herramientas gratuitas, conocidas y disponibles en Windows:

| Tecnologia | Uso |
|---|---|
| Python | Lenguaje principal del sistema. |
| Scapy | Captura y analisis de paquetes. |
| Flask | Dashboard web local. |
| Nmap | Generacion de trafico de prueba autorizado. |
| PowerShell/CMD | Automatizacion de ejecucion en Windows. |
| JSON/CSV | Persistencia y exportacion de registros. |

El sistema cuenta con archivos de arranque para simplificar la ejecucion:

- `setup_windows.ps1`: verifica Python, pip, dependencias y Nmap.
- `abrir_cmd_proyecto.bat`: inicia el dashboard.
- `abrir_powershell_admin.bat`: inicia el IDS como administrador.
- `abrir_powershell_pruebas.bat`: abre consola de pruebas.

**Resultado:** Factibilidad tecnica alta.

## 5. Factibilidad economica

El proyecto no requiere licencias comerciales. Los costos se limitan al uso de equipos personales, energia, internet y tiempo de desarrollo.

| Concepto | Costo estimado |
|---|---:|
| Herramientas de software | S/. 0.00 |
| Equipo de desarrollo propio | S/. 0.00 |
| Internet y energia | S/. 130.00 |
| Tiempo de desarrollo academico | S/. 1600.00 |
| Materiales y documentacion | S/. 275.00 |
| **Total estimado** | **S/. 2005.00** |

Frente a herramientas comerciales de monitoreo y seguridad, TrafficWatch IDS representa una alternativa de bajo costo para aprendizaje y pruebas.

**Resultado:** Factibilidad economica alta.

## 6. Factibilidad operativa

El sistema es operable por estudiantes con conocimientos basicos de redes y Windows. La ejecucion se simplifico mediante archivos `.bat`, de modo que el usuario puede iniciar dashboard, IDS y pruebas sin escribir comandos complejos.

Orden recomendado:

1. `abrir_cmd_proyecto.bat`
2. `abrir_powershell_admin.bat`
3. `abrir_powershell_pruebas.bat`

El dashboard permite interpretar los resultados mediante tablas, filtros, graficos y estado del IDS.

**Resultado:** Factibilidad operativa alta.

## 7. Factibilidad legal

El proyecto utiliza tecnologias open-source y se orienta a redes propias, laboratorios academicos o entornos autorizados. No realiza bloqueo de trafico ni acciones ofensivas. Las pruebas con Nmap y simuladores deben ejecutarse solo con autorizacion.

Los datos almacenados son tecnicos:

- Direcciones IP.
- Puertos.
- Protocolos.
- Flags TCP.
- Tipos de alerta.

**Resultado:** Factibilidad legal alta si se respeta el uso etico.

## 8. Factibilidad social y ambiental

El proyecto tiene impacto social positivo porque fortalece el aprendizaje practico en ciberseguridad, redes y calidad de software. Al ser software, no genera residuos fisicos ni requiere infraestructura adicional.

**Resultado:** Factibilidad social y ambiental alta.

## 9. Conclusiones

TrafficWatch IDS es viable desde el punto de vista tecnico, economico, operativo, legal, social y ambiental. La version actual cumple con el objetivo academico de capturar trafico, analizar patrones sospechosos, generar alertas, conservar evidencias y mostrar resultados mediante un dashboard local.

Se recomienda su uso en redes propias o laboratorios autorizados, manteniendo claramente su alcance como sistema IDS de deteccion y alerta.
