# Manual de uso de la skill TrafficWatch IDS

## Proposito

Este documento explica como usar la skill `trafficwatch-ids-review` y como se relaciona con los archivos de instrucciones para otras IAs.

La skill sirve para que Codex trabaje en TrafficWatch IDS con contexto del proyecto, reglas de seguridad, mapa de archivos, validaciones y prioridades de revision.

## Archivos de instrucciones

| Archivo | Uso principal |
|---|---|
| `.github/skills/trafficwatch-ids-review/SKILL.md` | Skill para Codex. |
| `.github/skills/trafficwatch-ids-review/agents/openai.yaml` | Nombre, descripcion corta y prompt sugerido de la skill en la interfaz. |
| `.github/copilot-instructions.md` | Instrucciones para GitHub Copilot dentro del repositorio. |
| `AGENTS.md` | Instrucciones generales para IAs que reconozcan archivos tipo AGENTS. |
| `.github/skills/trafficwatch-ids-review/AGENTS.md` | Copia de referencia para IAs generales dentro de la carpeta de la skill. |

## Como usar la skill en Codex

Para activar la skill en Codex, menciona su nombre con `$` en el prompt:

```text
Usa $trafficwatch-ids-review para revisar el dashboard.
```

Codex detecta `$trafficwatch-ids-review`, carga `SKILL.md` y trabaja siguiendo esas instrucciones.

## Formato recomendado

```text
Usa $trafficwatch-ids-review para [tarea concreta].
```

La tarea debe ser clara y especifica. Por ejemplo: revisar un archivo, actualizar documentacion, agregar una regla IDS, validar APIs o revisar compatibilidad con Render.

## Ejemplos de prompts

```text
Usa $trafficwatch-ids-review para revisar si web/app.py y dashboard.html tienen APIs consistentes.
```

```text
Usa $trafficwatch-ids-review para actualizar la documentacion FD04 segun el codigo actual.
```

```text
Usa $trafficwatch-ids-review para agregar una regla IDS nueva y actualizar las pruebas necesarias.
```

```text
Usa $trafficwatch-ids-review para revisar la respuesta activa antes de permitir bloqueos con Windows Firewall.
```

```text
Usa $trafficwatch-ids-review para comprobar que los cambios siguen siendo compatibles con Render.
```

## Que hace Codex al usar la skill

Cuando se usa la skill, Codex debe:

1. Leer `README.md`, `config.json` y los archivos relacionados con la tarea.
2. Revisar pruebas existentes antes de cambiar deteccion, almacenamiento, respuesta activa o dashboard.
3. Mantener separada la ejecucion local del IDS y la demostracion en Render.
4. Evitar usar logs reales como datos fuente o fixtures.
5. Mantener consistentes los tipos de alerta entre analizador, simulador, dashboard, respuesta activa y Suricata.
6. Proponer o ejecutar validaciones especificas segun el cambio.

## Que no debe hacer

La skill indica que no se deben ejecutar automaticamente:

- Capturas reales de red.
- Escaneos Nmap reales.
- Suricata real.
- Cambios de Windows Firewall.
- Instaladores o scripts de administrador.

Estas acciones solo deben hacerse si el usuario lo pide de forma explicita.

## Como usarlo con GitHub Copilot

GitHub Copilot no usa `SKILL.md` como Codex. Copilot toma contexto del repositorio y puede leer instrucciones generales desde:

```text
.github/copilot-instructions.md
```

Para usarlo:

1. Mantener actualizado `.github/copilot-instructions.md`.
2. Abrir el repositorio en VS Code con GitHub Copilot activo.
3. Pedir una tarea concreta en Copilot Chat.
4. Mencionar archivos cuando la tarea dependa de algo especifico.

Ejemplos:

```text
Revisa web/app.py y dashboard.html. Comprueba que las APIs usadas por el dashboard existan en Flask.
```

```text
Actualiza docs/FD04-Informe-Arquitectura de Software.md segun el codigo actual del proyecto.
```

```text
Revisa si estos cambios siguen siendo compatibles con Render. Ten en cuenta .github/copilot-instructions.md.
```

No es necesario invocar `$trafficwatch-ids-review` en Copilot. Esa sintaxis es para Codex. En Copilot basta con que el archivo `.github/copilot-instructions.md` exista y sea claro.

## Como usarlo con IAs generales

Las IAs generales normalmente no activan `SKILL.md` automaticamente. Para ellas se usa `AGENTS.md`, porque es un formato mas facil de reconocer como instrucciones del repositorio.

Hay dos opciones:

```text
AGENTS.md
```

Archivo general en la raiz del proyecto. Es la opcion recomendada si la IA trabaja sobre todo el repositorio.

```text
.github/skills/trafficwatch-ids-review/AGENTS.md
```

Copia de referencia dentro de la carpeta de la skill. Sirve si quieres mostrar la configuracion junto a `SKILL.md`.

Para usarlo con una IA general, escribe un prompt como:

```text
Lee AGENTS.md y sigue esas instrucciones para trabajar en este repositorio.
```

O, si quieres usar la copia dentro de la skill:

```text
Lee .github/skills/trafficwatch-ids-review/AGENTS.md y sigue esas instrucciones para trabajar en TrafficWatch IDS.
```

Despues agrega la tarea concreta:

```text
Luego revisa si el dashboard rompe alguna API de Flask.
```

```text
Luego actualiza la documentacion FD04 segun el codigo actual.
```

```text
Luego comprueba que los cambios sigan siendo compatibles con Render.
```

Si la IA no puede leer archivos del repositorio por si sola, copia el contenido de `AGENTS.md` en el chat y despues escribe la tarea.

## Resumen

- Para Codex: menciona `$trafficwatch-ids-review` en el prompt.
- Para Copilot: manten `.github/copilot-instructions.md` y pide la tarea en Copilot Chat.
- Para IAs generales: pide que lean `AGENTS.md` o copia su contenido en el chat.

La skill no es un programa independiente. Es una guia reutilizable para que Codex trabaje mejor dentro del proyecto TrafficWatch IDS.
