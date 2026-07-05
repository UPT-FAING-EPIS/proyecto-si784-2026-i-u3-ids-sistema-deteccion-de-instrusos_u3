![Logo](../media/logo-upt.png)

<!-- Archivo actualizado desde docs/FD04-EPIS-Informe Arquitectura de Software.docx -->

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

Escuela Profesional de Ingeniería de Sistemas

**SISTEMA DE DETECCION DE INSTRUSOS TRAFFICWATCH IDS**

Curso: Calidad y Pruebas de Software

Docente: Mag. Patrick Cuadros Quiroga

Integrantes:

Chara Apaza, Edgar Diego (2019065026)

Abel Fernando Pacompia Ortiz (2023076797)

Tacna – Perú

2026

### Control De Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| --- | --- | --- | --- | --- | --- |
| 2.0 | EDCA | APO | Cuadros Q. | 06/05/2026 | Versión Original |

Sistema de Detección de Intrusos TrafficWatch

Versión 2.0

### Control De Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| --- | --- | --- | --- | --- | --- |
| 1.0 | SNMY | JMP/ECA | MPV | 10/10/2020 | Versión Original |

**ÍNDICE GENERAL**

Contenido

**INTRODUCCIÓN**

Propósito (Diagrama 4+1)

El presente Documento de Arquitectura de Software (SAD) tiene como propósito describir la arquitectura del sistema TrafficWatch IDS, un sistema de detección de intrusos orientado al monitoreo de tráfico de red en redes pequeñas de la ciudad de Tacna.

La arquitectura se describe utilizando el modelo 4+1 de Philippe Kruchten, el cual contempla las siguientes vistas:

Vista de Casos de Uso: Describe los requerimientos funcionales y la interacción de los usuarios con el sistema.

Vista Lógica: Describe las clases, objetos y paquetes que conforman la estructura del sistema.

Vista de Procesos: Describe los procesos y flujos de ejecución del sistema.

Vista de Implementación: Describe los componentes de software y su organización.

Vista de Despliegue: Describe la distribución física del sistema sobre la infraestructura tecnológica.

Alcance

Este documento comprende la descripción arquitectónica del Sistema Web de Monitoreo y Gestión del Cloro Residual, utilizado para administrar información relacionada con centros poblados, sistemas de agua, mediciones de cloro residual, asistencias técnicas, alertas, reportes y dashboards de monitoreo.

El documento abarca:

Arquitectura lógica del sistema.

Arquitectura física y de despliegue.

Componentes de software.

Base de datos.

Diagramas UML de diseño.

Atributos de calidad del software.

Restricciones arquitectónicas.

No incluye detalles de programación ni manuales de usuario.

Definición, siglas y abreviaturas

| Término | Definición |
| --- | --- |
| SAD | Software Architecture Document, documento de arquitectura de software. |
| SRS | Software Requirements Specification, documento de especificación de requerimientos de software. |
| UML | Unified Modeling Language, lenguaje unificado de modelado. |
| IDS | Intrusion Detection System, sistema de detección de intrusos. |
| TrafficWatch IDS | Sistema propuesto para monitorear tráfico de red y detectar posibles intrusiones. |
| RF | Requerimiento Funcional. |
| RNF | Requerimiento No Funcional. |
| Dashboard | Panel gráfico que muestra alertas, estado del IDS, tráfico e indicadores. |
| Scapy | Librería de Python utilizada para capturar y analizar paquetes de red. |
| Flask | Framework de Python utilizado para desarrollar el dashboard web. |
| Python | Lenguaje de programación utilizado para desarrollar el sistema. |
| IP | Dirección lógica que identifica un dispositivo dentro de una red. |
| TCP | Protocolo de comunicación orientado a conexión. |
| UDP | Protocolo de comunicación no orientado a conexión. |
| ICMP | Protocolo usado para mensajes de control y diagnóstico de red. |
| JSON | Formato ligero para almacenar e intercambiar datos. |
| CSV | Formato de archivo separado por comas usado para exportar evidencias. |
| LAN | Red de área local. |
| Alerta | Notificación generada cuando el sistema detecta tráfico sospechoso. |
| Tráfico anómalo | Comportamiento de red fuera de lo normal o potencialmente sospechoso. |

Organización del documento

El presente Documento de Arquitectura de Software (SAD) se encuentra estructurado en capítulos que describen la arquitectura del Sistema Web de Gestión y Monitoreo de Cloro Residual en el Agua desde diferentes perspectivas, permitiendo comprender los componentes que conforman la solución y las decisiones de diseño adoptadas durante su construcción.

### Capítulo 1. Introducción

### Presenta el propósito, alcance, definiciones, referencias y organización general del documento, proporcionando el contexto necesario para comprender la arquitectura propuesta.

### Capítulo 2. Representación Arquitectónica

### Describe el enfoque arquitectónico utilizado en el sistema, así como los principios y patrones de diseño que servirán como base para la construcción de la solución.

### Capítulo 3. Objetivos y Restricciones de Arquitectura

### Define los objetivos arquitectónicos que debe cumplir el sistema y las restricciones tecnológicas, operativas y de desarrollo que condicionan su implementación.

### Capítulo 4. Vista Lógica

### Presenta la estructura funcional del sistema, los principales módulos de negocio, las entidades involucradas y las relaciones existentes entre los componentes que conforman la solución.

### Capítulo 5. Vista de Procesos

### Describe el comportamiento dinámico del sistema mediante diagramas y flujos de interacción, mostrando la ejecución de procesos y la comunicación entre componentes durante los principales casos de uso.

### Capítulo 6. Vista de Desarrollo

### Muestra la organización del software desde la perspectiva de implementación, incluyendo la distribución de paquetes, módulos, capas y componentes que conforman la aplicación bajo la arquitectura MVC.

### Capítulo 7. Vista Física

### Describe la infraestructura tecnológica requerida para el funcionamiento del sistema, incluyendo servidores, base de datos, dispositivos cliente, red de comunicaciones y servicios externos.

### Capítulo 8. Vista de Escenarios

### Presenta los principales escenarios arquitectónicos y casos de uso que permiten validar el comportamiento de la arquitectura propuesta frente a los requerimientos funcionales definidos en el SRS.

### Capítulo 9. Seguridad

### Describe los mecanismos de autenticación, autorización, control de acceso y protección de la información implementados para garantizar la seguridad del sistema.

### Capítulo 10. Conclusiones

### Resume los aspectos más relevantes de la arquitectura propuesta y los beneficios obtenidos mediante su aplicación en el desarrollo del sistema.

# OBJETIVOS Y RESTRICCIONES ARQUITECTÓNICAS

[Establezca las prioridades de los requerimientos y las restricciones del proyecto)

Priorización de requerimientos

| Código | Rol | Requerimiento Funcional | Descripción | Prioridad |
| --- | --- | --- | --- | --- |
| RF01 | Administrador | Monitorear tráfico de red | El sistema debe capturar tráfico de red en tiempo real dentro de una red local autorizada. | Alta |
| RF02 | Sistema | Detectar escaneo de puertos | El sistema debe identificar intentos de escaneo desde una IP hacia varios puertos. | Alta |
| RF03 | Sistema | Detectar fuerza bruta | El sistema debe detectar intentos repetidos de conexión hacia servicios como SSH, FTP, Telnet o RDP. | Alta |
| RF04 | Sistema | Detectar tráfico anómalo | El sistema debe identificar eventos como ICMP flood, SYN flood, tráfico sospechoso o conexiones frecuentes. | Alta |
| RF05 | Sistema | Generar alertas IDS | El sistema debe generar alertas con tipo de evento, IP origen, nivel de riesgo, descripción y fecha. | Alta |
| RF06 | Administrador | Visualizar dashboard web | El sistema debe mostrar alertas, estado del IDS, tráfico clasificado, gráficos e incidentes agrupados. | Alta |
| RF07 | Administrador | Consultar alertas e historial | El sistema debe permitir consultar el historial de alertas y eventos detectados. | Alta |
| RF08 | Sistema | Clasificar tráfico de red | El sistema debe clasificar el tráfico como local, externo, entrante, saliente o relacionado con la puerta de enlace. | Media |
| RF09 | Sistema | Agrupar incidentes | El sistema debe agrupar alertas repetidas o relacionadas para facilitar su análisis. | Media |
| RF10 | Administrador | Exportar evidencias | El sistema debe permitir exportar alertas y tráfico clasificado en formatos CSV y JSON. | Media |
| RF11 | Administrador | Ejecutar simulaciones controladas | El sistema debe permitir generar eventos de prueba para validar las reglas IDS. | Media |
| RF12 | Administrador | Realizar escaneo local controlado | El sistema debe permitir escanear dispositivos o puertos dentro de una red local autorizada. | Media |
| RF13 | Sistema | Integración con Suricata | El sistema debe permitir consultar eventos de Suricata y sugerir políticas IPS. | Baja |
| RF14 | Administrador | Respuesta activa manual | El sistema debe recomendar o aplicar acciones manuales autorizadas, como bloqueo temporal de IPs sospechosas. | Baja |
| RF15 | Administrador | Versión demostrativa en Render | El sistema debe permitir visualizar una versión web demostrativa sin captura real de red. | Baja |

### Requerimientos Funcionales

| Código | Requerimiento Funcional | Descripción | Prioridad |
| --- | --- | --- | --- |
| RF-01 | Monitorear tráfico de red | El sistema debe capturar paquetes de red en tiempo real dentro de una red local autorizada. | Alta |
| RF-02 | Detectar escaneo de puertos | El sistema debe identificar intentos de escaneo de puertos realizados desde una dirección IP. | Alta |
| RF-03 | Detectar fuerza bruta | El sistema debe detectar intentos repetidos de conexión hacia servicios como SSH, FTP, Telnet o RDP. | Alta |
| RF-04 | Detectar tráfico anómalo | El sistema debe identificar eventos como ICMP flood, SYN flood, conexiones frecuentes o puertos sospechosos. | Alta |
| RF-05 | Generar alertas de seguridad | El sistema debe generar alertas con tipo de evento, IP origen, nivel de riesgo, descripción y fecha. | Alta |
| RF-06 | Visualizar dashboard web | El sistema debe mostrar alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados. | Alta |
| RF-07 | Consultar alertas e historial | El sistema debe permitir consultar las alertas registradas durante el monitoreo. | Alta |
| RF-08 | Clasificar tráfico de red | El sistema debe clasificar el tráfico como entrante, saliente, local, externo o relacionado con la puerta de enlace. | Media |
| RF-09 | Agrupar incidentes | El sistema debe agrupar alertas repetidas o relacionadas para facilitar su análisis. | Media |
| RF-10 | Exportar evidencias | El sistema debe permitir exportar alertas y tráfico clasificado en formatos JSON y CSV. | Media |
| RF-11 | Ejecutar simulaciones controladas | El sistema debe permitir generar eventos de prueba controlados para validar las reglas IDS. | Media |
| RF-12 | Realizar escaneo local controlado | El sistema debe permitir realizar escaneo controlado de dispositivos o puertos dentro de la red local autorizada. | Media |
| RF-13 | Integrar eventos de Suricata | El sistema debe permitir consultar eventos de Suricata EVE y sugerir reglas o políticas IPS. | Baja |
| RF-14 | Aplicar respuesta activa manual | El sistema debe permitir recomendar o aplicar respuestas manuales autorizadas, como bloqueo temporal de IPs sospechosas. | Baja |
| RF-15 | Visualizar versión demostrativa en Render | El sistema debe permitir una versión web demostrativa para visualizar dashboard, historial, gráficos y simulaciones sin captura real de red. | Baja |

### Requerimientos No Funcionales – Atributos de Calidad

| Código | Requerimiento no funcional | Descripción |
| --- | --- | --- |
| RNF01 | Usabilidad | El sistema debe contar con una interfaz clara e intuitiva para que el administrador pueda revisar alertas, tráfico y estado del IDS fácilmente. |
| RNF02 | Seguridad | El sistema debe operar solo en redes autorizadas y respetar las direcciones IP monitoreadas. |
| RNF03 | Control de acceso | Las funciones de captura, escaneo y respuesta activa deben ser ejecutadas únicamente por el administrador autorizado. |
| RNF04 | Disponibilidad | El dashboard debe estar disponible mientras el sistema IDS se encuentre en ejecución. |
| RNF05 | Rendimiento | El sistema debe procesar y mostrar alertas en tiempos adecuados bajo condiciones normales de laboratorio. |
| RNF06 | Mantenibilidad | El sistema debe estar organizado por módulos para facilitar mejoras en reglas IDS, dashboard, almacenamiento y exportaciones. |
| RNF07 | Escalabilidad | El sistema debe permitir incorporar nuevas reglas de detección, tipos de alerta y módulos de análisis. |
| RNF08 | Compatibilidad | El dashboard debe funcionar en navegadores modernos como Chrome, Edge y Firefox. |
| RNF09 | Confiabilidad | El sistema debe registrar alertas e historial de forma consistente, evitando duplicados innecesarios. |
| RNF10 | Portabilidad | El sistema debe ejecutarse localmente en Windows y contar con una versión demostrativa compatible con Render. |

Restricciones

| Código | Restricción |
| --- | --- |
| RT01 | El sistema será desarrollado principalmente en Python. |
| RT02 | Se utilizará Flask para el dashboard web. |
| RT03 | Se utilizará Scapy para la captura y análisis de paquetes en entorno local autorizado. |
| RT04 | La información será almacenada en archivos JSON y podrá exportarse en CSV o JSON. |
| RT05 | La captura real de tráfico solo funcionará en entorno local con permisos adecuados. |
| RT06 | La versión en Render será únicamente demostrativa y no realizará captura real de red. |
| RT07 | No se deben ejecutar escaneos, capturas o bloqueos en redes externas sin autorización. |
| RT08 | El sistema debe funcionar en navegadores modernos para visualizar el dashboard. |

# REPRESENTACIÓN DE LA ARQUITECTURA DEL SISTEMA

La vista de caso de uso representa la interacción principal entre el Administrador y el sistema TrafficWatch IDS. Esta vista permite identificar las funcionalidades que el usuario puede realizar dentro del sistema, así como los procesos principales relacionados con el monitoreo de tráfico de red, detección de eventos sospechosos y visualización de información de seguridad.

En el sistema, el Administrador es el único actor principal y tiene acceso a las funciones de monitoreo, consulta, simulación y exportación. A través del dashboard web, puede visualizar el estado del IDS, revisar alertas, consultar el historial de eventos, ejecutar simulaciones controladas y exportar evidencias en formatos CSV o JSON

Vista de Caso de uso

Diagrama caso de Uso Monitorear trafico de Red

Diagrama caso de uso Visualizar dashboard web

Diagrama caso uso Consultar alertas e historial

Diagrama caso de uso ejecutar Simulaciones controladas

Diagrama caso de uso Exportar evidencias

Vista Lógica

### Diagrama de Subsistemas (paquetes)

### Diagrama de Secuencia (vista de diseño)

Diagrama secuencia Monitorear Trafico de red

Diagrama secuencia Visualizar dashboard web.

Diagrama secuencia Consultar Alertas e Historial

Diagrama secuencia Ejecutar Simulaciones controladas

Diagrama secuencia Exportar Evidencias.

### Diagrama de Colaboración (vista de diseño)

### Diagrama de Objetos

Monitorear tráfico de red.

Diagrama de objetos visualizar Dashboard

Consultar Alertas e historial

### Diagrama de Clases

### Diagrama de Base de datos (relacional o no relacional)

Vista de Implementación (vista de desarrollo)

### Diagrama de arquitectura software (paquetes)

### Diagrama de arquitectura del sistema (Diagrama de componentes)

Vista de procesos

### Diagrama de Procesos del sistema (diagrama de actividad)

Vista de Despliegue (vista física)

### Diagrama de despliegue

# ATRIBUTOS DE CALIDAD DEL SOFTWARE

.

Los atributos de calidad del software son propiedades medibles y evaluables que permiten determinar si el sistema cumple adecuadamente con las necesidades de los usuarios y stakeholders. En el caso del sistema TrafficWatch IDS, estos atributos permiten evaluar aspectos como funcionalidad, usabilidad, confiabilidad, rendimiento y mantenibilidad, los cuales son importantes para asegurar un correcto monitoreo de tráfico de red en entornos pequeños.

Escenario de Funcionalidad

El sistema TrafficWatch IDS debe permitir capturar tráfico de red dentro de una red local autorizada, analizar paquetes, detectar eventos sospechosos, generar alertas de seguridad y mostrar la información en un dashboard web.

Ejemplo:
El administrador inicia el monitoreo desde el sistema. TrafficWatch IDS captura paquetes de red, analiza el tráfico mediante reglas IDS y, si detecta un escaneo de puertos o intento de fuerza bruta, genera una alerta con la IP origen, tipo de evento, nivel de riesgo y fecha de detección.

Escenario de Usabilidad

El sistema debe ser fácil de usar para el administrador, permitiendo visualizar alertas, tráfico clasificado, historial e indicadores sin requerir conocimientos avanzados en ciberseguridad.

Ejemplo:
El administrador necesita revisar si hubo intentos de acceso sospechosos en la red local. Ingresa al dashboard web, revisa los gráficos de tráfico, consulta la tabla de alertas y filtra los eventos por nivel de riesgo o dirección IP.

Escenario de Confiabilidad

TrafficWatch IDS debe mantener la integridad de la información registrada, evitando pérdida de alertas o tráfico monitoreado. Además, debe garantizar que los datos almacenados en archivos JSON puedan consultarse correctamente desde el dashboard.

Ejemplo:
Si el sistema detecta varias alertas durante el monitoreo, estas deben registrarse correctamente en alerts.json. En caso de que un archivo presente errores o datos incompletos, el sistema debe manejar la situación sin detener completamente el dashboard.

Escenario de Rendimiento

El sistema debe procesar paquetes y mostrar información en el dashboard en tiempos aceptables, evitando retrasos excesivos durante el monitoreo de una red pequeña.

Ejemplo:
Durante una prueba en laboratorio, el sistema captura y analiza tráfico de red local, actualizando el dashboard en pocos segundos para que el administrador pueda observar alertas recientes y estado del IDS.

Escenario de Mantenibilidad

El sistema debe permitir realizar cambios o mejoras de forma sencilla, como agregar nuevas reglas de detección, modificar umbrales, actualizar vistas del dashboard o mejorar los reportes sin afectar el funcionamiento general.

Ejemplo:
Si se desea agregar una nueva regla para detectar tráfico sospechoso hacia un puerto específico, el desarrollador puede modificar el módulo de análisis y actualizar la configuración sin cambiar toda la estructura del sistema.

Otros Escenarios

Performance: TrafficWatch IDS debe responder adecuadamente ante eventos de red generados en un entorno pequeño, procesando tráfico local y mostrando alertas sin afectar de forma significativa el rendimiento del equipo.

Seguridad: El sistema debe utilizarse únicamente en redes autorizadas, respetando las direcciones IP y evitando acciones no permitidas sobre equipos externos.

Disponibilidad: El dashboard debe estar disponible mientras el sistema local se encuentre en ejecución, permitiendo al administrador consultar el estado del IDS, alertas e historial.
