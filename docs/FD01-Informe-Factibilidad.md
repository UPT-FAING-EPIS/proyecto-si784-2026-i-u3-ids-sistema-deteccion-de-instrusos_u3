![Logo](../media/logo-upt.png)

<!-- Archivo actualizado desde docs/FD01-EPIS-Informe de Factibilidad.docx -->

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

Sistema de Detección de Intrusos TrafficWatch IDS

Informe de Factibilidad

Versión 2.0

### Control De Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| --- | --- | --- | --- | --- | --- |
| 2.0 | EDCA | APO | Cuadros Q. | 06/05/2026 | Versión Original |

**INDICE GENERAL**

Descripción del Proyecto

Nombre del proyecto

Sistema de Detección de Intrusos TrafficWatch IDS

Duración del proyecto

Inicio de proyecto : 09 de abril

Fin de Proyecto : 24 de junio

: 85 días calendarío

Descripción

TrafficWatch IDS es un sistema académico de detección de intrusos desarrollado en Python, orientado al monitoreo de tráfico de red en entornos locales. El sistema captura paquetes mediante Scapy, analiza el tráfico usando reglas configurables y genera alertas cuando identifica comportamientos sospechosos, como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood, conexiones de alta frecuencia o uso de puertos sospechosos.

El proyecto incluye un dashboard web construido con Flask, donde se pueden visualizar las alertas generadas, el historial de eventos, gráficos estadísticos, estado del IDS, tráfico clasificado, incidentes agrupados y resultados de simulaciones controladas. Además, incorpora funciones complementarias como escaneo local controlado, integración con Suricata, generación de políticas IPS sugeridas y exportación de evidencias en formatos JSON y CSV.

TrafficWatch IDS está diseñado principalmente para fines académicos y de laboratorio. Su ejecución completa se realiza en Windows, mientras que también cuenta con una versión demostrativa desplegable en Render, destinada a mostrar el dashboard, simulaciones e historial sin depender de captura real de red, Nmap, Suricata ni acciones sobre el firewall. De esta manera, el sistema permite comprender de forma práctica el funcionamiento básico de un IDS, la clasificación del tráfico y la gestión de alertas de seguridad en una red local autorizada.

## 1.4 Objetivos

### 1.4.1 Objetivo general

Desarrollar un sistema de detección de intrusos, denominado TrafficWatch IDS, que permita monitorear tráfico de red en un entorno local, identificar comportamientos sospechosos mediante reglas configurables y visualizar alertas de seguridad a través de un dashboard web.

### 1.4.2 Objetivos Específicos

Implementar la captura de paquetes de red en tiempo real utilizando Python y Scapy.

Analizar el tráfico capturado mediante reglas IDS para detectar eventos sospechosos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia.

Clasificar el tráfico de red en categorías como entrante, saliente, local, externo y tráfico hacia la puerta de enlace.

Generar alertas de seguridad con información relevante sobre el tipo de evento, dirección IP, nivel de riesgo y fecha de detección.

Diseñar un dashboard web con Flask para visualizar alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados.

Incorporar funciones de apoyo como simulaciones controladas, escaneo local, integración con Suricata y generación de políticas IPS sugeridas.

Permitir la exportación de evidencias en formatos JSON y CSV para facilitar el análisis y la documentación académica.

Riesgos

| Riesgo | Descripción | Mitigación |
| --- | --- | --- |
| Falsos positivos | El sistema puede generar alertas ante tráfico legítimo que se asemeje a un comportamiento sospechoso. | Configurar umbrales adecuados, aplicar cooldown de alertas repetidas y realizar pruebas controladas. |
| Permisos insuficientes | La captura de paquetes con Scapy puede requerir permisos de administrador en Windows. | Ejecutar el sistema desde una consola con privilegios de administrador y documentar este requisito. |
| Dependencia de herramientas externas | Algunas funciones requieren Nmap, Npcap o Suricata instalados en el equipo local. | Mantener estas funciones como opcionales y validar su disponibilidad antes de ejecutarlas. |
| Limitaciones en Render | La versión desplegada en Render no puede capturar tráfico real, ejecutar Nmap, operar Suricata ni modificar el firewall local. | Usar Render solo como demostración web del dashboard, simulaciones e historial. |
| Uso indebido del sistema | El proyecto podría ser usado para pruebas en redes no autorizadas. | Documentar claramente que el sistema debe utilizarse únicamente en entornos propios, académicos o autorizados. |
| Pérdida o corrupción de logs | Los archivos JSON de alertas, tráfico o estado podrían dañarse durante la ejecución. | Implementar almacenamiento tolerante a errores y evitar usar logs reales como datos fijos de prueba. |
| Bloqueo incorrecto de IPs | Una acción de respuesta activa mal aplicada podría afectar la conectividad de equipos legítimos. | Mantener el bloqueo como acción manual, temporal y validada por el usuario. |
| Rendimiento limitado | En redes con alto volumen de tráfico, el sistema podría consumir más recursos o generar muchas alertas. | Usar reglas configurables, limitar el alcance académico del sistema y ajustar los umbrales según el entorno. |

Análisis de la Situación actual

Planteamiento del problema

En la actualidad, las redes locales se encuentran expuestas a diversos riesgos de seguridad, como escaneos de puertos, intentos de fuerza bruta, tráfico anómalo, conexiones repetitivas y posibles ataques de denegación de servicio. Sin embargo, en muchas redes pequeñas, domésticas, académicas o de pequeños negocios no existe un monitoreo constante sobre quién intenta ingresar a la red, qué dispositivos se comunican dentro de ella o qué comportamientos podrían representar una amenaza. Esta falta de supervisión puede ocasionar que actividades sospechosas pasen desapercibidas hasta que se produzca un incidente más evidente.

Esta problemática también puede presentarse en redes pequeñas de la ciudad de Tacna, donde muchas organizaciones, laboratorios, oficinas o usuarios particulares no cuentan con herramientas especializadas para observar el tráfico de red y detectar posibles intentos de intrusión. Además, las soluciones profesionales de seguridad suelen ser complejas, costosas o requieren conocimientos técnicos avanzados, lo que dificulta su adopción en este tipo de entornos.

Por ello, el sistema TrafficWatch IDS está diseñado para apoyar el monitoreo de redes pequeñas en la ciudad de Tacna, permitiendo analizar el tráfico de red en un entorno local autorizado, detectar comportamientos sospechosos mediante reglas configurables y presentar los resultados en una interfaz web clara. De esta forma, el proyecto facilita la identificación de alertas, la generación de evidencias y la comprensión práctica del funcionamiento básico de un sistema de detección de intrusos.

Consideraciones de hardware y software

Para la implementación y ejecución de TrafficWatch IDS, se consideran los recursos mínimos necesarios para que el sistema funcione correctamente en redes pequeñas de la ciudad de Tacna. Al tratarse de una herramienta académica y de laboratorio, el sistema no requiere una infraestructura empresarial compleja, pero sí necesita un equipo con capacidad suficiente para capturar tráfico, ejecutar el dashboard web y almacenar las alertas generadas.

### Hardware

| Recurso | Recomendación |
| --- | --- |
| Equipo principal | Computadora o laptop con sistema operativo Windows. |
| Procesador | Intel Core i3 o superior, o equivalente. |
| Memoria RAM | Mínimo 4 GB; recomendado 8 GB para mejor rendimiento. |
| Almacenamiento | Al menos 1 GB libre para el proyecto, dependencias y registros generados. |
| Tarjeta de red | Adaptador Ethernet o Wi-Fi compatible con captura de paquetes. |
| Red local | Conexión a una red pequeña doméstica, académica o de oficina. |

### Software

| Software | Uso dentro del proyecto |
| --- | --- |
| Windows | Sistema operativo principal para la ejecución local del IDS. |
| Python 3.9 o superior | Lenguaje usado para ejecutar el sistema. |
| Scapy | Captura y análisis de paquetes de red. |
| Flask | Desarrollo del dashboard web. |
| Npcap | Permite la captura de paquetes en Windows. |
| Nmap | Apoya el escaneo controlado de dispositivos y puertos en la red local. |
| Suricata | Herramienta complementaria para detección y análisis de eventos de seguridad. |
| Navegador web | Permite acceder al dashboard local del sistema. |
| Render | Plataforma usada únicamente para la demostración web del dashboard. |

Estudio de Factibilidad

En esta etapa se elabora el estudio de factibilidad del proyecto TrafficWatch IDS, con el propósito de determinar si la solución propuesta es viable tomando en cuenta los recursos técnicos, operativos y económicos disponibles. El sistema está orientado al monitoreo de redes pequeñas en la ciudad de Tacna, principalmente en entornos domésticos, académicos, oficinas o pequeños negocios que requieren una herramienta sencilla para observar el tráfico de red y detectar posibles comportamientos sospechosos.

Factibilidad Técnica

Se realizó la investigación necesaria en la Dirección Regional de Vivienda, para verificar la parte técnica y constatar la infraestructura tecnológica y de comunicaciones que se requiere, así como los recursos humanos, de esta manera se identificará los recursos técnicos que tiene la empresa. A continuación, se detalla lo encontrado.

**RECURSOS TÉCNICOS QUE TIENE LA EMPRESA**

La oficina de tecnologías de información cuenta con la siguiente infraestructura

| Hardware | Cantidad |
| --- | --- |
| PC_01 (detalle en la sección 3.2) | 4 |
| Impresora Epson L6171 | 1 |
| Parlantes | 1 |
| Switch TP-Link 32 puertos | 1 |
| Servidor HPE ProLiant DL380 | 1 |

| Software | Cantidad |
| --- | --- |
| Sistema Operativo Windows 10 Pro | 1 |
| Navegador Google Chrome | 1 |
| Office 2019 | 1 |

Con estos recursos se puede ejecutar el IDS en modo local, abrir el dashboard web, realizar simulaciones controladas, generar alertas, consultar el historial y exportar evidencias. Además, al contar con un laboratorio de pruebas, se garantiza que las validaciones se realicen en un ambiente autorizado, evitando afectar redes externas o dispositivos no relacionados con el proyecto.

Factibilidad Económica

Costos Generales

### Costos Generales

| Ítem | Descripción | u.m. | Costo Unitario | Cantidad | Costo Total |
| --- | --- | --- | --- | --- | --- |
| 1 | Papel Bond | Millar | S/ 20.00 | 2 | S/ 40.00 |
| 2 | Lapicero | Caja | S/ 5.00 | 10 | S/ 50.00 |
| 3 | Engrampador | Und. | S/ 15.00 | 1 | S/ 15.00 |
| 4 | Grapas | Caja | S/. 5.00 | 3 | S/. 15.00 |
| 5 | Perforador | Global | S/ 10.00 | 1 | S/ 10.00 |
| 6 | Folder | Global | S/. 0.80 | 10 | S/ 8.00 |
| 7 | Recarga de impresora | Und. | S/. 60.00 | 2 | S/. 120.00 |
| 8 | Archivador | Und. | S/. 15 | 2 | S/.30.00 |
| 9 | Resaltador | Und. | S/. 3 | 3 | S/. 9.00 |
|  | Total | S/ 297.00 |  |  |  |

Costos operativos durante el desarrollo

### Costos Operativos

| Ítem | Descripción | Costo Unitario | Meses | Total |
| --- | --- | --- | --- | --- |
| 1 | Agua | S/ 80.00 | 3 | S/ 240.00 |
| 2 | Luz | S/ 180.00 | 3 | S/ 540.00 |
| 3 | Internet | S/ 100.00 | 3 | S/ 300.00 |
|  | Total | S/ 1080.00 |  |  |

Costos de personal

### Costos De Personal

| Rol | Unidad | Cantidad | Costo Mes | Meses | Total | Horario de trabajo (L-V) | Horas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Arquitecto de Software | Und | 1 | S/ 1500.00 | 3 | S/ 4500.00 | 8:00 - 12:00 | 4 |
| Desarrollador | Und | 2 | S/ 1500.00 | 3 | S/ 4500.00 | 8:00 - 12:00 |  |
| Desarrollador | Und | 2 | S/ 1500.00 | 3 | S/ 4500.00 |  | 4 |
|  | Total | S/ 9,000.00 |  |  |  |  |  |

Costos totales del desarrollo del sistema

| Resumen de Costos | Costos Totales |
| --- | --- |
| Costos Generales | S/ 297.00 |
| Costos de Personal | S/ 9,000.00 |
| Costos Operativos | S/ 1080.00 |
| TOTAL | S/ 10.377.00 |

Factibilidad Operativa

La factibilidad operativa del proyecto TrafficWatch IDS se considera viable, debido a que el sistema está diseñado para ser utilizado en redes pequeñas de la ciudad de Tacna y en entornos de laboratorio académico. Su funcionamiento no requiere una infraestructura compleja, ya que puede ejecutarse desde una computadora con Windows conectada a una red local.

El sistema cuenta con un dashboard web que facilita la visualización de alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados. Esto permite que los usuarios puedan interpretar la información de seguridad de forma clara, sin necesidad de utilizar herramientas avanzadas de línea de comandos. Además, las funciones de simulación y laboratorio permiten generar eventos controlados para validar el comportamiento del sistema.

Desde el punto de vista del usuario, TrafficWatch IDS resulta operativo porque permite monitorear la red, identificar posibles comportamientos sospechosos y exportar evidencias en formatos JSON y CSV. Asimismo, el sistema mantiene separadas las funciones locales reales de la versión demostrativa en Render, evitando que la demo web dependa de captura real de red, Nmap, Suricata o acciones sobre el firewall.

Para su uso adecuado, se requiere que el usuario tenga conocimientos básicos sobre redes locales, direcciones IP, tráfico de red y seguridad informática. Sin embargo, el dashboard reduce la complejidad técnica al presentar la información de manera organizada y comprensible. Por ello, se concluye que el sistema puede ser operado de forma práctica en un laboratorio controlado o en una red pequeña autorizada

Beneficios operativos:

Permite monitorear el tráfico de red en redes pequeñas de forma local y controlada.

Facilita la detección de comportamientos sospechosos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia.

Presenta las alertas en un dashboard web claro y organizado, lo que mejora la interpretación de los eventos de seguridad.

Reduce la complejidad técnica mediante una interfaz visual que muestra historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados.

Permite realizar simulaciones controladas en laboratorio para validar el funcionamiento del sistema sin afectar redes externas.

Ayuda a generar evidencias mediante la exportación de alertas y tráfico clasificado en formatos JSON y CSV.

Contribuye al aprendizaje práctico sobre monitoreo de redes, detección de intrusos y análisis de tráfico.

Puede ejecutarse en una computadora con Windows dentro de una red pequeña, sin requerir una infraestructura empresarial compleja.

Mantiene separadas las funciones reales locales de la versión demostrativa en Render, evitando dependencias innecesarias en la nube.

Apoya la toma de decisiones al mostrar información relevante sobre posibles amenazas o actividades anómalas en la red.

Principales interesados:

Usuarios de redes pequeñas

Administradores de red

Institución académica

Área de Tecnologías de la Información

En conclusión, el sistema es operativamente factible, ya que mejora los procesos existentes y cuenta con el apoyo y capacidad de los usuarios para su implementación

Factibilidad Legal

El desarrollo e implementación del sistema TrafficWatch IDS se considera legalmente viable, siempre que sea utilizado únicamente en redes propias, autorizadas o en entornos de laboratorio académico. Al tratarse de una herramienta de monitoreo de tráfico de red, el sistema debe respetar la privacidad de las direcciones IP, dispositivos conectados y eventos registrados durante las pruebas.

En primer lugar, el sistema puede registrar información técnica como direcciones IP de origen y destino, puertos, tipo de tráfico, alertas generadas y fecha de detección. Por ello, esta información debe ser utilizada solo con fines académicos, preventivos y de análisis de seguridad dentro de una red autorizada. No se debe capturar, publicar ni compartir información de redes externas o usuarios que no hayan dado autorización.

Asimismo, TrafficWatch IDS no está diseñado para realizar ataques ni vulnerar sistemas ajenos. Sus funciones de escaneo, captura de paquetes, simulación y análisis deben ejecutarse únicamente en redes pequeñas controladas, como laboratorios, redes domésticas propias, oficinas autorizadas o entornos académicos. Esto permite evitar el uso indebido del sistema y proteger la privacidad de los equipos monitoreados.

El sistema utiliza herramientas legales y de uso permitido como Python, Flask, Scapy, Nmap, Npcap y Suricata, respetando sus licencias correspondientes. Estas herramientas se emplean con fines defensivos y educativos, orientados a detectar comportamientos sospechosos y comprender el funcionamiento de un IDS.

En ese sentido, no existen restricciones legales que impidan la ejecución del proyecto, siempre que se respete la privacidad de las direcciones IP y dispositivos monitoreados, se cuente con autorización para realizar pruebas y se mantenga el uso del sistema dentro de un entorno controlado. Por lo tanto, el proyecto se considera viable desde el punto de vista legal.

Factibilidad Social

El sistema también tiene un valor educativo, ya que permite a estudiantes y usuarios comprender de manera práctica cómo funciona un sistema de detección de intrusos, cómo se generan alertas y cómo se analiza el tráfico de red. Al contar con un dashboard web, la información se presenta de forma clara y comprensible, facilitando su uso incluso para personas con conocimientos básicos de redes.

Desde el punto de vista social, TrafficWatch IDS promueve el uso responsable de la tecnología, ya que está diseñado para emplearse únicamente en redes propias, autorizadas o en laboratorios controlados. Esto ayuda a fomentar buenas prácticas en seguridad informática, respeto por la privacidad de las direcciones IP y uso ético de herramientas de monitoreo.

En conclusión, el proyecto es socialmente viable porque responde a una necesidad real de supervisión básica en redes pequeñas, fortalece la formación académica en ciberseguridad y puede beneficiar a usuarios de Tacna que requieren una solución simple para observar posibles actividades sospechosas dentro de su red local.

Impactos sociales positivos:

Contribuye a mejorar la seguridad de redes pequeñas en la ciudad de Tacna.

Promueve la conciencia sobre la importancia de monitorear quién intenta ingresar a una red local.

Ayuda a usuarios de hogares, oficinas, laboratorios y pequeños negocios a identificar comportamientos sospechosos.

Fortalece el aprendizaje práctico de estudiantes en temas de redes, ciberseguridad y detección de intrusos.

Fomenta el uso ético y responsable de herramientas de monitoreo de tráfico de red.

Facilita la comprensión de alertas de seguridad mediante un dashboard web claro y organizado.

Permite realizar pruebas en laboratorios controlados sin afectar redes externas o dispositivos no autorizados.

Incentiva la protección de la privacidad de direcciones IP, dispositivos conectados y tráfico de red.

Brinda una alternativa accesible para entornos que no cuentan con soluciones profesionales de seguridad.

Apoya la prevención de incidentes al permitir una detección temprana de actividades anómalas.

Factibilidad Ambiental

El sistema presenta una factibilidad ambiental favorable, ya que su implementación contribuye a la reducción del impacto ambiental asociado a los procesos tradicionales basados en el uso de papel.

Al digitalizar el registro de monitoreos, se reduce el consumo de recursos como papel, tinta y otros materiales de oficina, lo cual disminuye la generación de residuos sólidos.

Adicionalmente, el sistema contribuye indirectamente a la protección del medio ambiente al garantizar un adecuado control del cloro residual en el agua, evitando tanto la sub cloración (riesgo sanitario) como la sobre cloración (impacto ambiental y en la salud).

Beneficios ambientales:

Reducción del uso de papel y materiales físicos

Disminución de residuos administrativos

Promoción de procesos digitales sostenibles

Mejora en el control de la calidad del agua

Análisis Financiero

El análisis financiero del proyecto TrafficWatch IDS permite identificar los costos estimados necesarios para su desarrollo, implementación y validación en un entorno de laboratorio controlado. Al tratarse de un sistema orientado a redes pequeñas de la ciudad de Tacna, el proyecto no requiere una inversión elevada en infraestructura especializada, ya que puede ejecutarse utilizando equipos de cómputo y herramientas de software disponibles.

Justificación de la Inversión

La inversión en el desarrollo del sistema se justifica debido a los beneficios que aporta en la mejora de la gestión del monitoreo de cloro residual en el agua, así como en la optimización de recursos y fortalecimiento institucional.

El costo del proyecto es relativamente bajo en comparación con el impacto positivo que genera, especialmente en términos de salud pública y eficiencia operativa.

### 5.1.1 Beneficios del Proyecto

Beneficios tangibles:

Reducción del tiempo de revisión manual del tráfico de red mediante alertas automáticas generadas por el sistema.

Mejora en la identificación de comportamientos sospechosos dentro de redes pequeñas, como escaneo de puertos, fuerza bruta, ICMP flood y conexiones de alta frecuencia.

Disminución del uso de papel mediante la generación y exportación de evidencias digitales en formatos JSON y CSV.

Mayor control sobre los eventos de seguridad registrados en la red local.

Reducción de pérdidas de información al almacenar alertas, historial y tráfico clasificado en archivos digitales.

Mejora en la organización de la información de seguridad mediante el dashboard web, gráficos e historial de eventos.

Beneficios intangibles:

Mejora en la conciencia sobre la importancia del monitoreo de redes pequeñas.

Fortalecimiento del aprendizaje práctico en redes, ciberseguridad y detección de intrusos.

Mayor confianza al contar con una herramienta que permite observar posibles intentos de ingreso no autorizado.

Toma de decisiones más rápida y oportuna frente a eventos sospechosos.

Promoción del uso ético y responsable de herramientas de monitoreo de tráfico.

Fortalecimiento de la seguridad informática en entornos domésticos, académicos, oficinas y pequeños negocios de Tacna.

Mayor comprensión del funcionamiento de un sistema IDS mediante una interfaz visual y accesible.

### 5.1.2 Criterios de Inversión

Para el proyecto TrafficWatch IDS, el principal criterio de inversión se basa en la optimización del tiempo destinado al monitoreo de redes pequeñas y en la reducción de costos asociados al uso de herramientas especializadas de seguridad. Al implementar el sistema, se automatiza la detección de comportamientos sospechosos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia, lo que permite disminuir la revisión manual del tráfico de red.

Asimismo, el sistema utiliza herramientas de software libre o de uso permitido, como Python, Flask, Scapy, Nmap y Suricata, lo que reduce costos de licenciamiento. También aprovecha recursos tecnológicos existentes en laboratorio, como computadoras, red local y navegadores web, evitando una inversión elevada en infraestructura adicional.

Por ello, la inversión se considera conveniente, ya que permite contar con una herramienta accesible para monitoreo de redes pequeñas en la ciudad de Tacna, mejora la capacidad de detección de eventos sospechosos, reduce el esfuerzo manual y contribuye al aprendizaje práctico en seguridad informática.

### 5.1.3 Análisis de Rentabilidad

El análisis de rentabilidad del proyecto TrafficWatch IDS permite evaluar si la inversión realizada genera beneficios suficientes en relación con los costos estimados. En este caso, la rentabilidad no solo se mide en términos económicos, sino también en beneficios operativos, académicos y de seguridad informática para redes pequeñas de la ciudad de Tacna.

El costo total estimado del proyecto asciende a S/ 10,377.00, considerando costos generales, costos de personal y costos operativos. Aunque el sistema no está orientado principalmente a generar ingresos directos, su rentabilidad se justifica por la reducción del esfuerzo manual en el monitoreo de red, el uso de herramientas de software libre, la generación de evidencias digitales y la prevención temprana de posibles incidentes de seguridad.

Para estimar la rentabilidad, se considera un ahorro operativo mensual aproximado de S/ 300.00, asociado a la disminución del tiempo destinado a revisar tráfico de red, analizar eventos y generar reportes manuales. Esto representa un ahorro anual de S/ 3,600.00 y un ahorro estimado de S/ 14,400.00 en un periodo de cuatro años.

| Periodo | Egresos (S/) | Ingresos / Ahorro (S/) | Flujo Neto (S/) |
| --- | --- | --- | --- |
| 0 | 10,377.00 | 0.00 | -10,377.00 |
| 1 | 120.00 | 3,600.00 | 3,480.00 |
| 2 | 120.00 | 3,600.00 | 3,480.00 |
| 3 | 120.00 | 3,600.00 | 3,480.00 |
| 4 | 120.00 | 3,600.00 | 3,480.00 |
| Total | 10,857.00 | 14,400.00 | 3,543.00 |

De acuerdo con la estimación realizada, el proyecto genera un flujo neto acumulado positivo de S/ 3,543.00 al cuarto año. Por lo tanto, TrafficWatch IDS se considera rentable dentro del periodo evaluado, ya que permite recuperar la inversión y obtener beneficios operativos adicionales.

#### 5.1.2.1 Relación Beneficio/Costo (B/C)

B/C = Beneficios totales / Costos totales

**B/C = 14,400.00 / 10,857.00**

**B/C = 1.33**

La relación Beneficio/Costo obtenida es 1.33, lo cual indica que por cada sol invertido se obtiene aproximadamente S/ 1.33 en beneficios. Como el resultado es mayor que 1, el proyecto se considera económicamente viable.

#### 5.1.2.2 Valor Actual Neto (VAN)

Para el cálculo del VAN se considera una tasa de descuento del 10% y un periodo de evaluación de 4 años.

| Periodo | Flujo Neto (S/) |
| --- | --- |
| 0 | -10,377.00 |
| 1 | 3,480.00 |
| 2 | 3,480.00 |
| 3 | 3,480.00 |
| 4 | 3,480.00 |

VAN = -10,377.00 + (3,480.00 / 1.10) + (3,480.00 / 1.10²) + (3,480.00 / 1.10³) + (3,480.00 / 1.10⁴)

**VAN = -10,377.00 + 3,163.64 + 2,876.03 + 2,614.57 + 2,376.88**

**VAN = 654.12**

El VAN obtenido es de S/ 654.12, por lo tanto, el proyecto TrafficWatch IDS resulta favorable desde el punto de vista financiero en un periodo de evaluación de cuatro años.

Conclusiones

El sistema TrafficWatch IDS permite monitorear redes pequeñas de manera local, identificando comportamientos sospechosos como escaneo de puertos, fuerza bruta, ICMP flood, SYN flood y conexiones de alta frecuencia.

El proyecto está orientado a redes pequeñas de la ciudad de Tacna, donde muchas veces no se cuenta con herramientas sencillas para observar quién intenta ingresar a la red o qué actividades pueden representar un riesgo.

El dashboard web facilita la visualización de alertas, historial, gráficos, estado del IDS, tráfico clasificado e incidentes agrupados, permitiendo una interpretación más clara de los eventos de seguridad.

El sistema puede ser probado en un laboratorio controlado con recursos disponibles, lo que demuestra su factibilidad técnica y operativa sin requerir una infraestructura empresarial compleja.

TrafficWatch IDS promueve el uso responsable de herramientas de monitoreo, respetando la privacidad de las direcciones IP y limitando su uso a redes propias, autorizadas o académicas.

El proyecto contribuye al aprendizaje práctico en ciberseguridad, redes y pruebas de software, ya que permite observar de forma real y controlada cómo funciona un sistema de detección de intrusos.

La solución resulta viable para su alcance académico, ya que utiliza herramientas accesibles como Python, Flask, Scapy, Nmap y Suricata, reduciendo costos de licenciamiento y facilitando su implementación.

En conclusión, TrafficWatch IDS es una herramienta útil, factible y educativa para mejorar el monitoreo básico de redes pequeñas, detectar posibles amenazas y fortalecer la cultura de seguridad informática en la ciudad de Tacna.
