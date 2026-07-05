![Logo](../media/logo-upt.png)

<!-- Archivo actualizado desde docs/FD03-EPIS-Informe Especificación Requerimientos.docx -->

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

Sistema de Detección de Intrusos TrafficWatch Documento de Especificación de Requerimientos de Software

Versión 2.0

# INTRODUCION

El presente documento de Especificación de Requerimientos de Software describe los requisitos funcionales y no funcionales del sistema TrafficWatch, un sistema de detección de intrusos orientado al monitoreo de redes pequeñas en la ciudad de Tacna. Este sistema tiene como finalidad identificar comportamientos sospechosos dentro de una red local, tales como escaneo de puertos, intentos de fuerza bruta, tráfico anómalo, ICMP flood, SYN flood y conexiones de alta frecuencia.

En muchas redes pequeñas, domésticas, académicas o de pequeños negocios no existe un monitoreo constante que permita conocer quién intenta ingresar a la red o qué actividades pueden representar una amenaza. Por ello, TrafficWatch propone una solución académica y práctica que permite capturar tráfico de red, analizarlo mediante reglas configurables y mostrar alertas de seguridad en un dashboard web claro y organizado.

El sistema será desarrollado utilizando tecnologías como Python, Scapy y Flask, permitiendo la captura de paquetes, el análisis de eventos y la visualización de resultados en una interfaz web. Además, contempla funciones como historial de alertas, gráficos, clasificación de tráfico, simulaciones controladas, exportación de evidencias e integración con herramientas complementarias como Nmap y Suricata.

Este documento servirá como guía para el análisis, diseño, desarrollo, prueba e implementación del sistema, estableciendo los alcances, restricciones, requerimientos y criterios necesarios para asegurar que TrafficWatch cumpla con los objetivos propuestos y contribuya al fortalecimiento de la seguridad informática en redes pequeñas autorizadas.

# GENERALIDADES DE LA EMPRESA

## Nombre de la empresa

## Universidad Privada de Tacna - Proyecto Académico de Calidad y Pruebas de Software y la evaluación de propuestas de gobierno.

## Visión

Ser una solución académica referente en el monitoreo de redes pequeñas, destacando por el uso de tecnologías de seguridad informática para la detección de comportamientos sospechosos, el análisis de tráfico de red y la generación de alertas que apoyen la prevención de incidentes en entornos locales

## Misión

## Desarrollar un sistema de detección de intrusos práctico y accesible, orientado a redes pequeñas de la ciudad de Tacna, que permita capturar y analizar tráfico de red, identificar posibles amenazas, visualizar alertas mediante un dashboard web y contribuir al aprendizaje, prevención y fortalecimiento de la seguridad informática. Organigrama

# VISIONAMIENTO DE LA EMPRESA

## Descripción del problema

En la ciudad de Tacna, muchas redes pequeñas, como las redes domésticas, académicas, oficinas y pequeños negocios, no cuentan con herramientas sencillas que permitan monitorear el tráfico de red y detectar posibles intentos de intrusión. En la mayoría de casos, los usuarios no revisan quién intenta ingresar a su red, qué dispositivos se comunican dentro de ella o qué comportamientos podrían representar una amenaza para la seguridad.

Esta situación genera que actividades sospechosas, como escaneos de puertos, intentos de fuerza bruta, tráfico anómalo, ICMP flood, SYN flood o conexiones repetitivas, puedan pasar desapercibidas. Además, las soluciones profesionales de seguridad informática suelen ser complejas, costosas o requieren conocimientos técnicos avanzados, lo cual dificulta su implementación en redes pequeñas o entornos académicos.

En el contexto de laboratorios de aprendizaje y redes locales autorizadas, también existe la necesidad de contar con una herramienta práctica que permita comprender cómo funciona un sistema de detección de intrusos, cómo se capturan los paquetes de red, cómo se generan alertas y cómo se visualizan los eventos de seguridad de manera clara.

Por ello, se propone el desarrollo de TrafficWatch, un sistema de detección de intrusos orientado a redes pequeñas de la ciudad de Tacna, que permita capturar y analizar tráfico de red, identificar comportamientos sospechosos mediante reglas configurables y presentar alertas de seguridad a través de un dashboard web accesible y organizado.

## Objetivos de negocios

### Objetivo general

Desarrollar un sistema de detección de intrusos, denominado TrafficWatch IDS, que permita monitorear tráfico de red en un entorno local, identificar comportamientos sospechosos mediante reglas configurables y visualizar alertas de seguridad a través de un dashboard web.

Objetivos específicos

Implementar la captura de paquetes de red en tiempo real utilizando Python y Scapy.

Analizar el tráfico capturado mediante reglas IDS para detectar eventos sospechosos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia.

Clasificar el tráfico de red en categorías como entrante, saliente, local, externo y tráfico hacia la puerta de enlace.

Generar alertas de seguridad con información relevante sobre el tipo de evento, dirección IP, nivel de riesgo y fecha de detección.

Diseñar un dashboard web con Flask para visualizar alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados.

Incorporar funciones de apoyo como simulaciones controladas, escaneo local, integración con Suricata y generación de políticas IPS sugeridas.

Permitir la exportación de evidencias en formatos JSON y CSV para facilitar el análisis y la documentación académica.

## Objetivo de diseño

Diseñar el sistema TrafficWatch como una herramienta de detección de intrusos orientada a redes pequeñas de la ciudad de Tacna, que permita monitorear el tráfico de red de forma local, identificar comportamientos sospechosos mediante reglas configurables y presentar la información de seguridad en un dashboard web claro, organizado y fácil de utilizar.

El diseño del sistema debe garantizar una arquitectura modular, separando la captura de paquetes, el análisis del tráfico, la gestión de alertas, el almacenamiento de evidencias y la visualización web. Asimismo, debe permitir su uso en laboratorios académicos y redes autorizadas, respetando la privacidad de las direcciones IP y manteniendo una experiencia sencilla para usuarios con conocimientos básicos de redes y seguridad informática

Alcance de proyecto

El proyecto TrafficWatch tiene como alcance el desarrollo de un sistema de detección de intrusos orientado al monitoreo de redes pequeñas en la ciudad de Tacna. El sistema permitirá capturar tráfico de red en un entorno local autorizado, analizarlo mediante reglas configurables y generar alertas cuando se identifiquen comportamientos sospechosos.

El sistema incluirá un dashboard web que permitirá visualizar alertas, historial de eventos, gráficos estadísticos, estado del IDS, tráfico clasificado e incidentes agrupados. Además, contará con funciones complementarias como simulaciones controladas, escaneo local de dispositivos, integración con herramientas de apoyo como Nmap y Suricata, y exportación de evidencias en formatos JSON y CSV.

El proyecto está enfocado en redes domésticas, académicas, oficinas o pequeños negocios, por lo que no busca reemplazar soluciones empresariales avanzadas de ciberseguridad. Su propósito principal es brindar una herramienta práctica, accesible y educativa para detectar posibles amenazas en redes pequeñas y fortalecer el aprendizaje en monitoreo de tráfico y detección de intrusos.

Queda fuera del alcance del proyecto el uso del sistema en redes externas sin autorización, la ejecución de ataques informáticos, el monitoreo masivo de redes empresariales de alta demanda y la aplicación automática de bloqueos sin validación del usuario. La versión web desplegada en Render será utilizada únicamente como demostración, sin captura real de tráfico ni acciones sobre el firewall.

## 2.5. Viabilidad del sistema

## El desarrollo del sistema de Dashboard de análisis electoral y evaluación de planes de gobierno - Perú 2026 es viable desde diferentes perspectivas, las cuales han sido analizadas en el estudio de factibilidad.

Viabilidad Técnica

El sistema TrafficWatch IDS es técnicamente viable, ya que puede desarrollarse e implementarse utilizando herramientas accesibles como Python, Scapy y Flask. Además, puede ejecutarse en una computadora con Windows conectada a una red local pequeña, permitiendo realizar pruebas en un laboratorio controlado. También puede apoyarse en herramientas como Npcap, Nmap y Suricata para fortalecer la captura, el escaneo controlado y el análisis de eventos de seguridad.

Viabilidad Económica

El proyecto es económicamente viable porque utiliza principalmente herramientas de software libre o de uso permitido, lo que reduce costos de licenciamiento. Asimismo, puede implementarse con equipos disponibles en laboratorio, sin requerir infraestructura empresarial compleja. La inversión se justifica por los beneficios que aporta en la reducción del tiempo de monitoreo manual, la generación de evidencias digitales y la detección temprana de comportamientos sospechosos.

Viabilidad Operativa

El sistema es operativamente viable porque cuenta con un dashboard web que facilita la visualización de alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados. Esto permite que los usuarios puedan interpretar la información de seguridad de manera clara, sin depender únicamente de herramientas técnicas o comandos avanzados. Además, puede utilizarse en redes pequeñas autorizadas y laboratorios académicos.

Viabilidad Legal

El sistema es legalmente viable siempre que sea utilizado únicamente en redes propias, autorizadas o de laboratorio. TrafficWatch IDS debe respetar la privacidad de las direcciones IP, dispositivos conectados y tráfico de red monitoreado. Sus funciones de captura, escaneo y análisis deben emplearse con fines académicos, preventivos y defensivos, evitando cualquier uso en redes externas sin autorización.

Viabilidad Social

El proyecto es socialmente viable porque contribuye a fortalecer la cultura de seguridad informática en redes pequeñas de la ciudad de Tacna. Permite que estudiantes, usuarios y administradores comprendan la importancia de monitorear quién intenta ingresar a una red y qué eventos pueden representar una amenaza. Además, promueve el aprendizaje práctico en redes, ciberseguridad y detección de intrusos.

Viabilidad Ambiental

El sistema es ambientalmente viable porque se trata de una solución de software que no genera residuos peligrosos ni requiere infraestructura física adicional. Además, permite registrar alertas, historial y evidencias en formato digital, reduciendo la necesidad de imprimir reportes físicos. Su ejecución puede realizarse con equipos ya disponibles, evitando la adquisición innecesaria de nuevos dispositivos.

# ANALISIS DE PROCESOS

## Diagrama del proceso actual – diagrama de actividades

## Diagrama de proceso propuesto – diagrama de actividades inicial

En el proceso propuesto, el usuario inicia TrafficWatch IDS en una computadora conectada a una red local autorizada. El sistema detecta la interfaz de red, IP local, gateway y red, para luego capturar tráfico mediante Scapy.

El tráfico capturado es analizado con reglas IDS configurables. Si no se detecta actividad sospechosa, el sistema clasifica el tráfico normal y actualiza el dashboard. Si se identifica un comportamiento sospechoso, se genera una alerta de seguridad, se registra evidencia, se agrupa como incidente si corresponde y se muestra en el dashboard web.

Finalmente, el usuario puede revisar la alerta, exportar evidencias o aplicar una respuesta manual autorizada, manteniendo el uso del sistema dentro de un entorno controlado y seguro.

# ESPECIFICACION DE REQUERIMIENTOS DE SOFTWARE

# Cuadro de requerimientos funcional inicial

| Código | Requerimiento Funcional | Descripción | Prioridad |
| --- | --- | --- | --- |
| RF01 | Captura de tráfico de red | El sistema debe capturar paquetes de red en tiempo real dentro de una red local autorizada utilizando Scapy. | Alta |
| RF02 | Detección de comportamientos sospechosos | El sistema debe analizar el tráfico capturado para identificar eventos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia. | Alta |
| RF03 | Generación de alertas de seguridad | El sistema debe generar alertas cuando detecte comportamientos sospechosos, indicando tipo de alerta, dirección IP, nivel de riesgo y fecha del evento. | Alta |
| RF04 | Visualización de alertas en dashboard | El sistema debe mostrar las alertas generadas en un dashboard web claro y organizado. | Alta |
| RF05 | Consulta de historial de eventos | El sistema debe permitir consultar el historial de alertas y eventos registrados durante el monitoreo. | Alta |
| RF06 | Clasificación del tráfico de red | El sistema debe clasificar el tráfico como entrante, saliente, local, externo o relacionado con la puerta de enlace. | Media |
| RF07 | Visualización de gráficos estadísticos | El sistema debe mostrar gráficos sobre alertas, tipos de tráfico y eventos detectados para facilitar el análisis. | Media |
| RF08 | Exportación de evidencias | El sistema debe permitir exportar alertas y tráfico clasificado en formatos JSON y CSV. | Media |
| RF09 | Simulación de eventos controlados | El sistema debe permitir generar eventos de prueba controlados para validar el funcionamiento de las reglas IDS. | Media |
| RF10 | Integración con herramientas de apoyo | El sistema debe permitir el uso complementario de herramientas como Nmap y Suricata para fortalecer el análisis de seguridad. | Baja |

## Cuadro de requerimiento no funcionales

| Código | Requerimiento No Funcional | Descripción | Prioridad |
| --- | --- | --- | --- |
| RNF01 | Usabilidad | El sistema debe contar con un dashboard web claro, organizado y fácil de usar para usuarios con conocimientos básicos de redes. | Alta |
| RNF02 | Rendimiento | El sistema debe mostrar alertas, historial y gráficos en un tiempo adecuado, evitando demoras excesivas durante el monitoreo. | Alta |
| RNF03 | Disponibilidad | El dashboard debe estar disponible mediante navegador web mientras el sistema se encuentre en ejecución local. | Alta |
| RNF04 | Compatibilidad | El sistema debe funcionar en Windows y poder visualizarse en navegadores modernos como Chrome, Edge o Firefox. | Alta |
| RNF05 | Seguridad | El sistema debe utilizarse solo en redes autorizadas y debe proteger la información técnica registrada, como direcciones IP, puertos y eventos detectados. | Alta |
| RNF06 | Privacidad | El sistema debe respetar la privacidad de las direcciones IP y dispositivos monitoreados, evitando compartir información de redes externas o no autorizadas. | Alta |
| RNF07 | Mantenibilidad | El sistema debe permitir la actualización de reglas IDS, configuración, dashboard y módulos sin afectar el funcionamiento general. | Media |
| RNF08 | Portabilidad | El sistema debe poder ejecutarse en un entorno local con Windows y contar con una versión demostrativa compatible con Render. | Media |
| RNF09 | Confiabilidad | El sistema debe registrar alertas e historial de forma consistente, evitando pérdida de información durante la ejecución. | Media |
| RNF10 | Escalabilidad | El sistema debe permitir la incorporación de nuevas reglas de detección, tipos de alertas y funciones complementarias en futuras versiones. | Media |

## Cuadro de requerimientos funcionales final

| Código | Requerimiento Funcional | Descripción | Prioridad |
| --- | --- | --- | --- |
| RF01 | Captura de tráfico de red | El sistema debe capturar paquetes de red en tiempo real dentro de una red local autorizada utilizando Scapy. | Alta |
| RF02 | Detección de escaneo de puertos | El sistema debe identificar intentos de escaneo de puertos realizados desde una dirección IP hacia varios puertos del equipo monitoreado. | Alta |
| RF03 | Detección de fuerza bruta | El sistema debe detectar intentos repetidos de conexión hacia servicios como SSH, FTP, Telnet o RDP. | Alta |
| RF04 | Detección de tráfico anómalo | El sistema debe identificar eventos como ICMP flood, SYN flood, conexiones de alta frecuencia y uso de puertos sospechosos. | Alta |
| RF05 | Generación de alertas de seguridad | El sistema debe generar alertas con información relevante como tipo de evento, IP origen, nivel de riesgo, descripción y fecha de detección. | Alta |
| RF06 | Visualización de dashboard web | El sistema debe mostrar en un dashboard las alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados. | Alta |
| RF07 | Consulta de historial de alertas | El sistema debe permitir consultar el historial de alertas registradas durante el monitoreo. | Alta |
| RF08 | Clasificación de tráfico | El sistema debe clasificar el tráfico de red como entrante, saliente, local, externo o relacionado con la puerta de enlace. | Media |
| RF09 | Agrupación de incidentes | El sistema debe agrupar alertas repetidas o relacionadas para facilitar su análisis en el dashboard. | Media |
| RF10 | Exportación de evidencias | El sistema debe permitir exportar alertas y tráfico clasificado en formatos JSON y CSV. | Media |
| RF11 | Simulación de eventos controlados | El sistema debe permitir generar eventos de prueba controlados para validar el funcionamiento de las reglas IDS. | Media |
| RF12 | Escaneo local controlado | El sistema debe permitir realizar escaneo controlado de dispositivos o puertos dentro de la red local autorizada. | Media |
| RF13 | Integración con Suricata | El sistema debe permitir consultar eventos de Suricata EVE y generar reglas o políticas IPS sugeridas. | Baja |
| RF14 | Respuesta activa manual | El sistema debe permitir recomendar o aplicar respuestas manuales autorizadas, como bloqueo temporal de IPs sospechosas. | Baja |
| RF15 | Versión demostrativa en Render | El sistema debe permitir una versión web demostrativa en Render para visualizar dashboard, historial, gráficos y simulaciones sin captura real de red. | Baja |

## Reglas de negocio

| Código | Regla de Negocio | Descripción |
| --- | --- | --- |
| RN01 | Uso autorizado del sistema | TrafficWatch IDS solo debe utilizarse en redes propias, autorizadas o en laboratorios académicos. |
| RN02 | Privacidad de direcciones IP | Las direcciones IP, puertos y eventos registrados deben mantenerse privados y no deben compartirse sin autorización. |
| RN03 | Captura en entorno local | La captura real de paquetes solo debe ejecutarse en una red local autorizada y desde un equipo con los permisos necesarios. |
| RN04 | Generación de alertas | El sistema debe generar una alerta cuando el tráfico cumpla alguna regla IDS configurada. |
| RN05 | Clasificación de alertas | Toda alerta debe clasificarse según su tipo, nivel de riesgo, dirección IP y fecha de detección. |
| RN06 | Control de alertas repetidas | El sistema debe aplicar un tiempo de espera o cooldown para evitar alertas duplicadas o demasiado frecuentes. |
| RN07 | Registro de historial | Toda alerta o evento relevante debe guardarse en el historial para su posterior revisión. |
| RN08 | Exportación de evidencias | Las alertas y registros solo deben exportarse con fines académicos, preventivos o de análisis autorizado. |
| RN09 | Escaneo controlado | Los escaneos de red solo deben realizarse dentro de la red local autorizada. |
| RN10 | Respuesta activa manual | Las acciones de bloqueo o respuesta ante una amenaza deben ser manuales, temporales y autorizadas por el usuario. |
| RN11 | Separación entre local y Render | La versión local puede capturar tráfico real, mientras que la versión en Render solo debe funcionar como demostración web. |
| RN12 | Uso ético del sistema | El sistema no debe utilizarse para atacar, vulnerar o analizar redes externas sin permiso. |

# FASE DE DESARROLLO

## Perfiles de usuario

| Perfil de Usuario | Descripción | Funciones Principales |
| --- | --- | --- |
| Administrador del sistema | Usuario encargado de instalar, configurar y ejecutar TrafficWatch IDS en una red local autorizada. | Configurar el sistema, iniciar la captura, revisar alertas, gestionar evidencias y aplicar acciones manuales autorizadas. |
| Usuario de red pequeña | Persona que utiliza una red doméstica, académica, oficina o pequeño negocio y desea conocer posibles actividades sospechosas. | Consultar el dashboard, revisar alertas, observar gráficos e interpretar el estado de la red. |

## Modelo conceptual

### Diagrama de paquetes

El modelo conceptual representa los paquetes principales del sistema y la relación entre actores, funcionalidades y requerimientos. Los diagramas permiten observar el alcance funcional de TrafficWatch IDS antes de pasar al detalle técnico de implementación.

### Diagramas de casos de uso

Diagrama caso de Uso Monitorear trafico de Red

Diagrama caso de uso Visualizar dashboard web

Diagrama caso uso Consultar alertas e historial

Diagrama caso de uso ejecutar Simulaciones controladas

Diagrama caso de uso Exportar evidencias

### Escenario de casos de usos (narrativa)

| Campo | Descripción |
| --- | --- |
| Id Caso de Uso | CU-01 |
| Nombre | Monitorear tráfico de red |
| Tipo | Obligatorio ( X ) / Opcional ( ) |
| Requisito ID (RF) | RF-01 |
| Versión | 1 |
| Autor | Equipo de Desarrollo |
| Actores | Administrador |
| Interacción | Fase de Elaboración |
| Descripción | Permitir al administrador iniciar el monitoreo del tráfico de red en una red local autorizada, capturando paquetes en tiempo real para su posterior análisis mediante reglas IDS. |
| Referencias | Diagrama caso de uso Monitorear tráfico de red |
| Anexos | Ninguno |
| Precondiciones | 1. El sistema TrafficWatch IDS debe estar instalado. <br>2. El equipo debe estar conectado a una red local autorizada. <br>3. El administrador debe contar con permisos necesarios para capturar tráfico. <br>4. Las dependencias de captura deben estar disponibles. |
| Postcondiciones | 1. El sistema inicia el monitoreo de red. <br>2. Los paquetes capturados quedan disponibles para análisis. <br>3. El estado del IDS se actualiza como activo. |

| Administrador | Sistema |
| --- | --- |
| 1. Ejecuta TrafficWatch IDS en el equipo local. | 2. Carga la configuración inicial del sistema. |
| 3. Solicita iniciar el monitoreo de tráfico de red. | 4. Detecta la interfaz de red, IP local, gateway y red disponible. |
| 5. Confirma el inicio del monitoreo. | 6. Inicia la captura de paquetes en tiempo real mediante Scapy. |
| 7. Mantiene el sistema en ejecución. | 8. Analiza el tráfico capturado mediante reglas IDS configuradas. |
| 9. Revisa el estado del monitoreo. | 10. Actualiza el estado del IDS y muestra la información en el dashboard. |

| Administrador | Sistema |
| --- | --- |
| 1. Solicita iniciar el monitoreo de red. | 2. Detecta que no existen permisos suficientes para capturar tráfico. |
| 3. Espera respuesta del sistema. | 4. Muestra el mensaje: “No se pudo iniciar la captura. Ejecute el sistema con permisos de administrador”. |

| Administrador | Sistema |
| --- | --- |
| 1. Solicita iniciar el monitoreo de red. | 2. No detecta una interfaz de red válida. |
| 3. Revisa el mensaje del sistema. | 4. Muestra el mensaje: “No se encontró una interfaz de red disponible para el monitoreo”. |

Narrativa caso de uso Visualizar Dashboard

| Campo | Descripción |
| --- | --- |
| Id Caso de Uso | CU-02 |
| Nombre | Visualizar dashboard web |
| Tipo | Obligatorio ( X ) / Opcional ( ) |
| Requisito ID (RF) | RF-06 |
| Versión | 1 |
| Autor | Equipo de Desarrollo |
| Actores | Administrador |
| Interacción | Fase de Elaboración |
| Descripción | Permitir al administrador acceder al dashboard web de TrafficWatch IDS para visualizar alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados. |
| Referencias | Diagrama caso de uso Visualizar dashboard web |
| Anexos | Ninguno |
| Precondiciones | 1. El sistema TrafficWatch IDS debe estar en ejecución. <br>2. El dashboard Flask debe estar disponible. <br>3. El administrador debe acceder desde un navegador web compatible. |
| Postcondiciones | 1. El dashboard muestra la información principal del sistema. <br>2. El administrador puede revisar alertas, historial, gráficos y estado del IDS. <br>3. La información queda disponible para nuevas consultas. |

Flujo Normal de Eventos

| Administrador | Sistema |
| --- | --- |
| 1. Abre el navegador web. | 2. Mantiene disponible el servidor Flask del dashboard. |
| 3. Ingresa a la URL del dashboard. | 4. Carga la página principal de TrafficWatch IDS. |
| 5. Selecciona la sección que desea revisar. | 6. Consulta la información registrada en alertas, historial, tráfico y estado. |
| 7. Revisa las alertas, gráficos e indicadores mostrados. | 8. Presenta la información en tablas, tarjetas y gráficos visuales. |
| 9. Continúa navegando por el dashboard. | 10. Actualiza la información disponible para nuevas consultas. |

Flujo de Excepción E001

| Administrador | Sistema |
| --- | --- |
| 1. Intenta acceder al dashboard web. | 2. Detecta que el servidor Flask no está disponible. |
| 3. Espera respuesta del navegador. | 4. No se puede cargar la página del sistema. |

Flujo de Excepción E002

| Administrador | Sistema |
| --- | --- |
| 1. Ingresa al dashboard. | 2. Detecta que no existen alertas o registros disponibles. |
| 3. Revisa la pantalla principal. | 4. Muestra tablas vacías o mensajes indicando que no hay información registrada. |

Narrativa de caso de uso Consultar alertas e historial

| Campo | Descripción |
| --- | --- |
| Id Caso de Uso | CU-03 |
| Nombre | Consultar alertas e historial |
| Tipo | Obligatorio ( X ) / Opcional ( ) |
| Requisito ID (RF) | RF-07 |
| Versión | 1 |
| Autor | Equipo de Desarrollo |
| Actores | Administrador |
| Interacción | Fase de Elaboración |
| Descripción | Permitir al administrador consultar las alertas generadas por el sistema y revisar el historial de eventos registrados durante el monitoreo de la red. |
| Referencias | Diagrama caso de uso Consultar alertas e historial |
| Anexos | Ninguno |
| Precondiciones | 1. El sistema debe estar en ejecución. <br>2. El dashboard web debe estar disponible. <br>3. Deben existir alertas o registros generados, o el sistema debe mostrar el historial vacío. |
| Postcondiciones | 1. El administrador visualiza las alertas registradas. <br>2. El sistema muestra información como tipo de alerta, IP origen, nivel de riesgo, descripción y fecha. <br>3. El historial queda disponible para nuevas consultas o exportación. |

Flujo Normal de Eventos

| Administrador | Sistema |
| --- | --- |
| 1. Accede al dashboard web de TrafficWatch IDS. | 2. Carga la información disponible del sistema. |
| 3. Selecciona la sección de alertas o historial. | 4. Consulta los registros almacenados. |
| 5. Revisa la lista de alertas generadas. | 6. Muestra tipo de alerta, IP origen, nivel de riesgo, descripción y fecha. |
| 7. Aplica filtros si necesita ubicar una alerta específica. | 8. Filtra los resultados por tipo, IP, nivel o fecha. |
| 9. Consulta el detalle de una alerta o incidente. | 10. Muestra la información detallada del evento seleccionado. |

Narrativa de caso de uso Simulaciones controladas

| Campo | Descripción |
| --- | --- |
| Id Caso de Uso | CU-04 |
| Nombre | Ejecutar simulaciones controladas |
| Tipo | Obligatorio ( ) / Opcional ( X ) |
| Requisito ID (RF) | RF-11 |
| Versión | 1 |
| Autor | Equipo de Desarrollo |
| Actores | Administrador |
| Interacción | Fase de Elaboración |
| Descripción | Permitir al administrador ejecutar simulaciones controladas para generar eventos de prueba y validar el funcionamiento de las reglas IDS, alertas y visualización en el dashboard. |
| Referencias | Diagrama caso de uso Ejecutar simulaciones controladas |
| Anexos | Ninguno |
| Precondiciones | 1. El sistema TrafficWatch IDS debe estar en ejecución. <br>2. El dashboard web debe estar disponible. <br>3. El administrador debe realizar la simulación en un entorno autorizado o de laboratorio. |
| Postcondiciones | 1. El sistema registra el evento simulado. <br>2. Se genera una alerta o resultado de prueba. <br>3. El administrador puede revisar el resultado en el dashboard. |

| Administrador | Sistema |
| --- | --- |
| 1. Accede al dashboard web de TrafficWatch IDS. | 2. Carga las secciones disponibles del sistema. |
| 3. Ingresa a la sección de simulaciones o Attack Lab. | 4. Muestra las opciones de simulación disponibles. |
| 5. Selecciona el tipo de simulación controlada. | 6. Prepara los parámetros necesarios para la prueba. |
| 7. Ejecuta la simulación. | 8. Genera un evento de prueba dentro del entorno autorizado. |
| 9. Revisa el resultado de la simulación. | 10. Registra la alerta o resultado y lo muestra en el dashboard. |

Narrativa de caso de uso Exportar evidencias

| Campo | Descripción |
| --- | --- |
| Id Caso de Uso | CU-05 |
| Nombre | Exportar evidencias |
| Tipo | Obligatorio ( ) / Opcional ( X ) |
| Requisito ID (RF) | RF-10 |
| Versión | 1 |
| Autor | Equipo de Desarrollo |
| Actores | Administrador |
| Interacción | Fase de Elaboración |
| Descripción | Permitir al administrador exportar alertas, historial o tráfico clasificado como evidencias digitales en formatos JSON o CSV para su análisis y documentación. |
| Referencias | Diagrama caso de uso Exportar evidencias |
| Anexos | Ninguno |
| Precondiciones | 1. El sistema TrafficWatch IDS debe estar en ejecución. <br>2. El dashboard web debe estar disponible. <br>3. Deben existir registros, alertas o tráfico clasificado para exportar. |
| Postcondiciones | 1. El sistema genera un archivo de evidencia en formato JSON o CSV. <br>2. El administrador descarga o guarda el archivo exportado. <br>3. La evidencia queda disponible para análisis o documentación académica. |

| Administrador | Sistema |
| --- | --- |
| 1. Accede al dashboard web de TrafficWatch IDS. | 2. Carga las secciones disponibles del sistema. |
| 3. Ingresa a la sección de alertas, historial o tráfico clasificado. | 4. Muestra los registros disponibles para exportación. |
| 5. Selecciona la opción de exportar. | 6. Permite elegir el formato de exportación JSON o CSV. |
| 7. Confirma la exportación de evidencias. | 8. Genera el archivo con la información registrada. |
| 9. Descarga o guarda el archivo generado. | 10. Entrega el archivo exportado al administrador. |

## Modelo logico

### Analisis de objetos

El análisis de objetos permite identificar los elementos principales que intervienen en los casos de uso del sistema TrafficWatch IDS. Para este análisis se consideran tres tipos de objetos: objetos de interfaz, objetos de control y objetos de datos.

Los objetos de interfaz representan las pantallas o formularios mediante los cuales el administrador interactúa con el sistema. Los objetos de control representan la lógica encargada de procesar la información, ejecutar reglas IDS, gestionar alertas o generar reportes. Finalmente, los objetos de datos representan la información almacenada por el sistema, como alertas, tráfico capturado, historial, estado del IDS y archivos exportados.

Diagrama de objetos Monitorear tráfico de red.

 Visualizar dashboard web

 Consultar alertas e historial

 Ejecutar simulaciones controladas

 Exportar evidencias

### Diagrama de actividades con objetos

diagrama de actividades con objetos permite representar el flujo principal del sistema TrafficWatch IDS y los objetos que se generan, consultan o actualizan durante el proceso. En este caso, se muestra cómo el administrador inicia el sistema, se carga la configuración, se captura el tráfico, se analiza mediante reglas IDS y se actualiza el dashboard con la información obtenida.

Diagrama de Objetos Monitorear trafico de red

Diagrama de Objetos Dashboard Web

Diagrama de Objetos Dashboard Web

Diagrama de Objetos Ejecutar simulaciones

Diagrama de Objetos Exportar Evidencias

### Diagrama de secuencia

Diagrama de secuencia - Monitorear tráfico de red,

Diagrama de secuencia de Visualizar dashboard web

Diagrama de secuencia - Consultar alertas e historial.

Diagrama de secuencia - Ejecutar simulaciones controladas.

Diagrama de secuencia - Exportar evidencias.

### Diagrama de clases

El diagrama de clases representa la estructura lógica del sistema TrafficWatch IDS. El Administrador interactúa con el DashboardWeb para monitorear el tráfico, visualizar alertas, consultar historial, ejecutar simulaciones y exportar evidencias.

El SistemaIDS coordina la captura y análisis del tráfico de red mediante las clases Capturador Paquetes y AnalizadorIDS. Cuando se detecta una actividad sospechosa, el Gestor Alertas genera alertas que se almacenan en la Base Datos. Además, el sistema cuenta con módulos de Simulador Eventos, Exportador Evidencias y ReporteDashboard, que permiten validar el IDS, generar archivos CSV/JSON y mostrar indicadores visuales.

diagrama de clases de Monitorear tráfico de red.

Diagrama de clases visualizar Dashboard

Diagrama de clases Consultar alertas

## 6. CONCLUSIONES

El desarrollo del sistema TrafficWatch IDS permite monitorear el tráfico de red en redes pequeñas de la ciudad de Tacna, facilitando la detección de posibles intentos de intrusión, escaneo de puertos, fuerza bruta y tráfico anómalo.

El sistema responde a la problemática identificada, ya que muchas redes pequeñas no cuentan con herramientas de monitoreo constantes ni prestan suficiente atención a los intentos de acceso no autorizado. Mediante alertas, historial, dashboard y exportación de evidencias, se mejora la visibilidad de la seguridad de la red.

A través de los requerimientos, casos de uso, análisis de objetos y diagramas UML, se logró definir la estructura funcional y lógica del sistema, proporcionando una base clara para su implementación con Python, Scapy y Flask.

Finalmente, el proyecto demuestra viabilidad técnica, operativa, económica, legal, social y ambiental, debido al uso de herramientas accesibles, pruebas en laboratorio controlado y una propuesta orientada a fortalecer la seguridad informática en redes pequeñas.

## 7. RECOMENDACIONES

Se recomienda continuar con la mejora del sistema priorizando las funciones principales, como la captura de tráfico, detección de anomalías, generación de alertas y visualización del dashboard web.

También se recomienda realizar pruebas en redes locales autorizadas y ambientes de laboratorio, evitando ejecutar capturas o escaneos en redes externas sin permiso.

Asimismo, se sugiere ajustar periódicamente las reglas y umbrales de detección para reducir falsos positivos y mejorar la precisión del sistema IDS.

Finalmente, se recomienda considerar mejoras futuras, como integración con más herramientas de seguridad, reportes automáticos, notificaciones en tiempo real y opciones avanzadas de respuesta ante incidentes.

## 8. BIBLIOGRAFÍA

Sommerville, I. (2011). Ingeniería de Software. Pearson Educación.

Pressman, R. S. (2010). Ingeniería del Software: Un enfoque práctico. McGraw-Hill.

Stallings, W. (2017). Network Security Essentials: Applications and Standards. Pearson.

Kurose, J. F., & Ross, K. W. (2017). Redes de computadoras: Un enfoque descendente. Pearson.

## 9. WEBGRAFÍA

Python Software Foundation. Documentación oficial de Python: https://www.python.org/doc/

Flask. Documentación oficial: https://flask.palletsprojects.com/

Scapy. Documentación oficial: https://scapy.readthedocs.io/

Suricata. Documentación oficial: https://suricata.io/documentation/

Render. Documentación oficial: https://render.com/docs
