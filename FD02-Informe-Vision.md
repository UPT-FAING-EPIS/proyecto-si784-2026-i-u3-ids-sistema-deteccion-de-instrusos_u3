<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *TrafficWatch IDS***

Curso: *CALIDAD Y PRUEBAS DE SOFTWARE*

Docente: *MAG.PATRICK CUADROS QUIROGA*

Integrantes:

***Edgar Diego Chara Apaza        (2019065026)***

***Abel Fernando Pacompía Ortiz   (2023076797)***


**Tacna – Perú**

***2026***

**  
**
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|04/04/2026|Versión Original|












**Sistema *Desarrollo de un sistema de detección de intrusos (IDS) para monitoreo de tráfico de red***

**Documento de Visión**

**Versión *{1.0}***
**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|04/04/20260|Versión Original|


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


**INDICE GENERAL**
#
[1.	Introducción](#_Toc52661346)

1.1	Propósito

1.2	Alcance

1.3	Definiciones, Siglas y Abreviaturas

1.4	Referencias

1.5	Visión General

[2.	Posicionamiento](#_Toc52661347)

2.1	Oportunidad de negocio

2.2	Definición del problema

[3.	Descripción de los interesados y usuarios](#_Toc52661348)

3.1	Resumen de los interesados

3.2	Resumen de los usuarios

3.3	Entorno de usuario

3.4	Perfiles de los interesados

3.5	Perfiles de los Usuarios

3.6	Necesidades de los interesados y usuarios

[4.	Vista General del Producto](#_Toc52661349)

4.1	Perspectiva del producto

4.2	Resumen de capacidades

4.3	Suposiciones y dependencias

4.4	Costos y precios

4.5	Licenciamiento e instalación

[5.	Características del producto](#_Toc52661350)

[6.	Restricciones](#_Toc52661351)

[7.	Rangos de calidad](#_Toc52661352)

[8.	Precedencia y Prioridad](#_Toc52661353)

[9.	Otros requerimientos del producto](#_Toc52661354)

b) Estandares legales

c) Estandares de comunicación	](#_toc394513800)37

d) Estandaraes de cumplimiento de la plataforma	](#_toc394513800)42

e) Estandaraes de calidad y seguridad	](#_toc394513800)42

[CONCLUSIONES](#_Toc52661355)

[RECOMENDACIONES](#_Toc52661356)

[BIBLIOGRAFIA](#_Toc52661357)

[WEBGRAFIA](#_Toc52661358)


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**<u>Informe de Visión</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Introducción**

        1.1	Propósito
   
El presente documento de visión tiene como propósito describir de manera general el sistema TrafficWatch IDS, un sistema de detección de intrusos (IDS) orientado al monitoreo del tráfico de red. Este documento define el alcance del sistema, los problemas que busca resolver, los actores involucrados y las necesidades que se pretenden satisfacer.

Asimismo, sirve como base para la planificación, desarrollo y validación del sistema, permitiendo al equipo de trabajo y a los interesados comprender claramente los objetivos del proyecto.


    1.2	Alcance

El sistema TrafficWatch IDS está orientado al monitoreo de redes locales en entornos académicos o de pequeña escala, permitiendo identificar actividades sospechosas mediante el análisis del tráfico de red en tiempo real.

El sistema incluirá funcionalidades como:

- Captura de paquetes de red
- Análisis de tráfico mediante reglas simples
- Detección de comportamientos anómalos
- Generación de alertas


        1.3	Definiciones, Siglas y Abreviaturas

- IDS (Intrusion Detection System): Sistema que permite detectar actividades sospechosas en una red.
- Tráfico de red: Conjunto de datos que circulan por una red informática.
- Paquete: Unidad básica de información transmitida en una red.
- IP: Dirección que identifica un dispositivo en la red.
- Puerto: Punto lógico de comunicación en un sistema.
- Scapy: Librería de Python para manipulación y análisis de paquetes de red.


        1.4	Referencias

- Documentación oficial de Python
- Documentación de la librería Scapy
- Material del curso de Calidad y Pruebas de Software
- Documentación interna del proyecto


        1.5	Visión General

El documento está organizado en secciones que describen el contexto del proyecto, los problemas identificados, los usuarios involucrados y las características generales del sistema. Primero se presenta el posicionamiento del sistema, seguido de la descripción de los interesados y usuarios, permitiendo tener una visión clara del propósito y utilidad del sistema IDS.


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>



2. <span id="_Toc52661347" class="anchor"></span>**Posicionamiento**

        2.1	Oportunidad de negocio

En la actualidad, la seguridad informática se ha convertido en una necesidad fundamental debido al incremento de ataques en redes. Sin embargo, muchas instituciones educativas y pequeñas organizaciones no cuentan con herramientas accesibles para monitorear su red.

Las soluciones comerciales de seguridad suelen ser costosas y complejas, lo que limita su implementación en entornos académicos.

El desarrollo de TrafficWatch IDS representa una oportunidad para ofrecer una solución accesible, educativa y funcional que permita:
- Mejorar la seguridad en redes locales
- Facilitar el aprendizaje en ciberseguridad
- Reducir costos al utilizar software open-source



        2.2	Definición del problema

Actualmente, muchas redes no cuentan con mecanismos adecuados para detectar intrusiones en tiempo real.

Esto genera problemas como:
- Accesos no autorizados sin detección
- Falta de control sobre el tráfico de red
- Dificultad para identificar ataques
- Dependencia de herramientas costosas

¿Cómo detectar actividades sospechosas en una red sin utilizar soluciones complejas o costosas?
El proyecto propone resolver este problema mediante un sistema IDS básico, capaz de monitorear tráfico y generar alertas de manera eficiente.



<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. <span id="_Toc52661348" class="anchor"></span>**Vista General del Producto**

        3.1	Resumen de los interesados

Los interesados del proyecto son aquellas personas o grupos que se ven afectados por el desarrollo o el resultado del sistema, aunque no necesariamente lo utilicen de forma directa:

| Nombre                 | Descripción                                                                 | Responsabilidades |
|------------------------|-----------------------------------------------------------------------------|------------------|
| Equipo de desarrollo   | Estudiantes encargados de diseñar e implementar el sistema IDS.            | Diseño, desarrollo, pruebas y mantenimiento del sistema. |
| Docente del curso      | Profesor encargado de supervisar y evaluar el proyecto.                    | Evaluar avances, validar resultados y guiar el desarrollo. |
| Institución académica  | Universidad donde se desarrolla el proyecto.                               | Brindar entorno académico y recursos básicos para el desarrollo. |
| Comunidad técnica      | Personas interesadas en seguridad informática y software open-source.      | Analizar, reutilizar o mejorar el sistema desarrollado. |



    3.2	Resumen de los usuarios

Los usuarios directos del sistema son aquellos que interactuarán con el IDS para monitorear el tráfico de red y detectar posibles amenazas:

| Nombre              | Descripción                                                                 | Responsabilidades | Comentarios |
|--------------------|-----------------------------------------------------------------------------|------------------|------------|
| Estudiante usuario | Persona que utiliza el sistema con fines académicos.                        | Ejecutar el sistema y analizar las alertas generadas. | Usuario principal del sistema. |
| Desarrollador      | Persona que implementa y mejora el sistema IDS.                             | Configurar reglas, optimizar el sistema y realizar pruebas. | Usuario técnico. |
| Analista de red    | Usuario con conocimientos básicos de redes.                                 | Interpretar el tráfico de red y validar alertas. | Uso intermedio. |




    3.3	Entorno de usuario
    
El sistema será utilizado en un entorno académico controlado:

| Elemento           | Descripción |
|--------------------|------------|
| Hardware           | Laptops o PCs con mínimo 4GB RAM |
| Sistema operativo  | Windows o Linux (Linux recomendado) |
| Red                | LAN o Wi-Fi |
| Herramientas       | Python, VS Code, Scapy |
| Tipo de entorno    | Académico y de pruebas |



    3.4	Perfiles de los interesados

| Interesado         | Perfil |
|-------------------|-------|
| Docente           | Profesional encargado de evaluar el proyecto y asegurar el cumplimiento académico. |
| Institución       | Organización que promueve el desarrollo de proyectos tecnológicos. |
| Comunidad técnica | Grupo interesado en software open-source. |


    3.5	Perfiles de los Usuarios

| Usuario           | Perfil |
|------------------|-------|
| Estudiante       | Usuario con conocimientos básicos de redes que utiliza el sistema con fines educativos. |
| Desarrollador    | Usuario técnico que implementa y mejora el sistema. |
| Analista de red  | Usuario que interpreta el tráfico y evalúa amenazas. |



    3.6	Necesidades de los interesados y usuarios

| Tipo de necesidad | Descripción |
|------------------|------------|
| Seguridad        | Detectar intrusiones y actividades sospechosas en la red. |
| Simplicidad      | Sistema fácil de usar e implementar. |
| Accesibilidad    | Uso de herramientas gratuitas y open-source. |
| Monitoreo        | Visualización del tráfico en tiempo real. |



<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de
    Factibilidad**

            4.1	Perspectiva del producto

El sistema TrafficWatch IDS se concibe como una solución independiente de software orientada al monitoreo y análisis de tráfico de red en entornos académicos. No forma parte de un sistema mayor, sino que funciona como una herramienta autónoma que puede integrarse de manera complementaria con infraestructuras de red existentes en laboratorios, aulas o redes institucionales.

El producto se ejecutará en equipos con sistema operativo compatible con Python, permitiendo la captura y análisis de paquetes en tiempo real mediante la biblioteca Scapy. Su arquitectura está orientada a la simplicidad y modularidad, facilitando su comprensión, mantenimiento y posible ampliación futura.

Asimismo, el sistema podrá ser utilizado como base para prácticas académicas relacionadas con seguridad informática, redes y análisis de tráfico, contribuyendo al aprendizaje práctico de los estudiantes.

    4.2	Resumen de capacidades

El sistema TrafficWatch IDS contará con las siguientes capacidades principales:

- Captura de tráfico de red en tiempo real:
Permite interceptar paquetes que circulan en la red utilizando la biblioteca Scapy.

- Análisis de paquetes:
Examina características relevantes del tráfico como direcciones IP, puertos, protocolos y frecuencia de envío.

- Detección de actividades sospechosas:
Identifica comportamientos como escaneo de puertos, múltiples intentos de conexión o patrones anómalos de tráfico.

- Generación de alertas:
Notifica al usuario cuando se detecta una posible intrusión o actividad inusual.

- Registro de eventos:
Almacena información relevante de las detecciones para su posterior análisis.

- Interfaz simple de uso:
Presenta la información de manera clara (consola o interfaz básica), facilitando la interpretación de los resultados.

- Facilidad de configuración:
Permite ajustar parámetros como umbrales de detección o tipos de alertas.



          4.3	Suposiciones y dependencias

Para el correcto funcionamiento del sistema, se consideran las siguientes suposiciones y dependencias:

Suposiciones:
- El sistema será utilizado en un entorno académico controlado.
- Los usuarios cuentan con conocimientos básicos de redes y seguridad informática.
- El volumen de tráfico a analizar será moderado.
- El sistema no requiere un nivel de precisión equivalente a soluciones comerciales avanzadas.
  
Dependencias:
- Instalación previa de Python 3 en el sistema.
- Uso de la biblioteca Scapy para la captura y análisis de paquetes.
- Permisos de administrador o privilegios elevados para la captura de tráfico de red.
- Sistema operativo compatible (Linux o Windows con configuración adecuada).
- Acceso a una red activa para realizar el monitoreo.


        4.4	Costos y precios
  
| Categoría              | Descripción                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| Enfoque del proyecto | Proyecto académico sin fines comerciales                                    |
| Desarrollo           | Realizado por estudiantes, sin costo económico directo                      |
| Herramientas         | Uso de software libre: Python, Scapy, Visual Studio Code                    |
| Infraestructura      | Equipos personales o recursos de la institución                             |
| Precio del producto  | Gratuito                                                                    |
| Tipo de distribución | Open-source, orientado a fines educativos              


    4.5	Licenciamiento e instalación

### Licenciamiento

| Aspecto      | Descripción                                                                 |
|-------------|-----------------------------------------------------------------------------|
| Tipo        | Código abierto                                                              |
| Licencia    | MIT o GPL                                                                   |
| Permisos    | Uso, modificación y distribución libre con fines educativos                 |

### Instalación

| Paso | Descripción                                                                 |
|------|-----------------------------------------------------------------------------|
| 1    | Clonar el repositorio desde GitHub                                          |
| 2    | Instalar Python 3                                                           |
| 3    | Instalar dependencias (Scapy) usando `pip`                                  |
| 4    | Ejecutar el sistema desde consola o entorno de desarrollo                   |

### Requisitos mínimos

| Requisito              | Descripción                         |
|-----------------------|-------------------------------------|
| Sistema operativo     | Windows o Linux                    |
| Lenguaje             | Python 3.x                         |
| Permisos             | Administrador (captura de paquetes)|
| Red                  | Conexión activa                    |







<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

5. <span id="_Toc52661350" class="anchor"></span>**Características del producto**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

El sistema **TrafficWatch IDS** contará con un conjunto de funcionalidades orientadas al monitoreo, análisis y detección de intrusiones en redes académicas. Estas características han sido definidas considerando la simplicidad, accesibilidad y utilidad educativa del sistema.

         5.1 Captura de tráfico de red
         
El sistema permitirá capturar paquetes de datos en tiempo real utilizando la biblioteca Scapy, posibilitando el análisis continuo del tráfico que circula por la red.

         5.2 Análisis de paquetes
         
Se realizará el análisis de información relevante contenida en los paquetes, tales como direcciones IP, puertos de origen y destino, protocolos y frecuencia de transmisión.

         5.3 Detección de intrusiones
         
El sistema identificará patrones de comportamiento sospechoso, tales como:
- Escaneo de puertos
- Múltiples intentos de conexión en corto tiempo
- Tráfico inusual o anómalo

         5.4 Generación de alertas
  
Cuando se detecte una posible intrusión, el sistema generará alertas en tiempo real, notificando al usuario mediante mensajes en consola o interfaz básica.

         5.5 Registro de eventos
         
Se almacenarán los eventos detectados en archivos de registro, permitiendo su revisión posterior para análisis o fines académicos.

         5.6 Configuración del sistema
         
El usuario podrá ajustar parámetros como:
- Umbrales de detección
- Tipos de alertas
- Frecuencia de monitoreo


6. <span id="_Toc52661351" class="anchor"></span>**Restricciones**

El desarrollo e implementación del sistema **TrafficWatch IDS** está sujeto a diversas restricciones técnicas, académicas y operativas:

- El sistema será desarrollado en un plazo limitado de 1 mes.
- Se utilizarán únicamente herramientas de software libre.
- El sistema no está diseñado para entornos de alta demanda o producción.
- Dependencia de Python y la biblioteca Scapy.
- Requiere permisos de administrador para la captura de paquetes.
- Limitaciones en precisión y cobertura en comparación con sistemas IDS comerciales.
- Uso restringido a entornos académicos y controlados.
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


7. <span id="_Toc52661352" class="anchor"></span>**Rangos de Calidad**

Para el desarrollo del sistema, se consideran las siguientes suposiciones:

- Los usuarios tienen conocimientos básicos de redes y seguridad informática.
- El entorno de uso será controlado (laboratorios o redes académicas).
- El volumen de tráfico será moderado.
- Los equipos utilizados cumplen con los requisitos mínimos del sistema.
- El sistema será utilizado con fines educativos y no críticos.
- Existirá disponibilidad de conexión de red para las pruebas.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

8. <span id="_Toc52661353" class="anchor"></span>**Precedencia y Prioridad**

El sistema **TrafficWatch IDS** deberá cumplir con los siguientes atributos de calidad:

        8.1 Usabilidad

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Facilidad de uso | El sistema debe ser sencillo de utilizar por usuarios con conocimientos básicos |
| Interfaz     | Presentación clara de la información en consola o interfaz básica           |
| Comprensión  | Las alertas deben ser fáciles de interpretar                                |



        8.2 Rendimiento

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Tiempo real  | Capacidad de analizar tráfico en tiempo real                                |
| Eficiencia   | Bajo consumo de recursos del sistema                                        |
| Respuesta    | Generación rápida de alertas ante eventos sospechosos                       |



        8.3 Fiabilidad

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Estabilidad  | Funcionamiento continuo sin fallos durante el monitoreo                     |
| Integridad   | Correcto registro de eventos sin pérdida de datos                           |
| Consistencia | Resultados coherentes ante condiciones similares                            |



         8.4 Mantenibilidad

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Modularidad  | Código organizado en módulos independientes                                 |
| Documentación| Código documentado para facilitar mantenimiento                             |
| Escalabilidad| Facilidad para agregar nuevas funcionalidades                               |



         8.5 Portabilidad

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Compatibilidad | Funcionamiento en sistemas Windows y Linux                                |
| Instalación  | Proceso sencillo en diferentes entornos                                     |
| Adaptabilidad| Capacidad de ejecutarse en distintos equipos sin modificaciones mayores     |



         8.6 Seguridad

| Atributo     | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Control de acceso | Uso de permisos adecuados para captura de paquetes                     |
| Protección de datos | Resguardo básico de logs y registros generados                    |
| Uso responsable | Evitar ejecución en redes sin autorización                             |




<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

9. <span id="_Toc52661354" class="anchor"></span>**Otros requerimientos del producto**

        9.1 Requisitos legales
   
El sistema no deberá vulnerar normas legales relacionadas con la privacidad y el uso de redes. Su uso estará limitado a entornos autorizados.


        9.2 Requisitos éticos
        
El sistema será utilizado únicamente con fines educativos, evitando el uso indebido para monitoreo no autorizado o actividades maliciosas.


        9.3 Requisitos de documentación
        
El proyecto incluirá documentación técnica y de usuario que permita:
- Comprender el funcionamiento del sistema
- Instalar correctamente el software
- Utilizar sus funcionalidades

        9.4 Requisitos de implementación
  
- Uso del lenguaje Python 3
- Implementación con la biblioteca Scapy
- Control de versiones mediante GitHub
- Desarrollo en entorno Visual Studio Code


        9.5 Requisitos de pruebas
  
El sistema deberá ser validado mediante pruebas básicas que permitan verificar:
- Captura correcta de paquetes
- Detección de patrones sospechosos
- Generación de alertas
- Registro de eventos

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>



<span id="_Toc52661355" class="anchor"></span>**CONCLUSIONES**

El desarrollo del sistema **TrafficWatch IDS** permitió aplicar conceptos fundamentales de seguridad informática y análisis de tráfico de red en un entorno práctico y académico. A través de la implementación del sistema, se logró comprender el funcionamiento básico de un sistema de detección de intrusos (IDS), así como la importancia del monitoreo continuo en la identificación de actividades sospechosas.

Asimismo, el uso de herramientas como Python y la biblioteca Scapy demostró que es posible desarrollar soluciones funcionales de bajo costo, accesibles y adaptadas a contextos educativos. El sistema cumple con los objetivos planteados, permitiendo la captura de paquetes, el análisis de tráfico y la generación de alertas ante posibles intrusiones.

Por otro lado, el proyecto evidenció las limitaciones propias de una solución académica, tales como la precisión en la detección, la escalabilidad y la falta de integración con sistemas más complejos. Sin embargo, estas limitaciones no afectan su valor como herramienta de aprendizaje.

En conclusión, **TrafficWatch IDS** constituye una base sólida para futuros desarrollos en el área de seguridad de redes, promoviendo el aprendizaje práctico y el interés en la ciberseguridad.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


<span id="_Toc52661356" class="anchor"></span>**RECOMENDACIONES**

Se recomienda continuar con el desarrollo del sistema **TrafficWatch IDS**, incorporando mejoras que incrementen su funcionalidad, precisión y aplicabilidad en entornos más complejos.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>



<span id="_Toc52661357" class="anchor"></span>**BIBLIOGRAFIA**

- Sommerville, I. (2011). *Ingeniería de software* (9ª ed.). Pearson Educación.

- Stallings, W. (2017). *Seguridad informática: principios y práctica*. Pearson.

- Kurose, J., & Ross, K. (2017). *Redes de computadoras: un enfoque descendente* (7ª ed.). Pearson.

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


<span id="_Toc52661358" class="anchor"></span>**WEBGRAFIA**
- Python Software Foundation. (2026). *Python Documentation*.  
  https://docs.python.org/3/

- Scapy Project. (2026). *Scapy Documentation*.  
  https://scapy.readthedocs.io/

- OWASP Foundation. (2026). *Open Web Application Security Project*.  
  https://owasp.org/

- Cisco Networking Academy. (2026). *Introducción a la Ciberseguridad*.  
  https://www.netacad.com/

- NIST. (2026). *Guide to Intrusion Detection and Prevention Systems*.  
  https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf

- GeeksforGeeks. (2026). *Intrusion Detection System (IDS)*.  
  https://www.geeksforgeeks.org/intrusion-detection-system-ids/

- IBM Security. (2026). *What is an Intrusion Detection System (IDS)?*  
  https://www.ibm.com/topics/intrusion-detection-system

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
