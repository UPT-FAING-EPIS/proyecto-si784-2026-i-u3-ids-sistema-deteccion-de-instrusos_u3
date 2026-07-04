# Tareas resueltas en GitHub Project

Este archivo resume las tareas que deben figurar como cerradas o en estado `Done` dentro del GitHub Project del curso.

> Nota: el tablero GitHub Project pertenece a la organizacion `UPT-FAING-EPIS`. Si la cuenta no tiene permisos sobre Projects, solo un owner/admin del proyecto puede mover o cerrar items en el tablero.

## Tareas sugeridas para marcar como Done

| Tarea | Evidencia en el repositorio | Estado esperado |
|---|---|---|
| Configurar portal de reportes QA en GitHub Pages | `.github/workflows/deploy-pages.yml` y rama `gh-pages` | Done |
| Publicar pruebas unitarias en GitHub Pages | `unit-tests/index.html`, `unit-tests/pytest-report.html` | Done |
| Publicar cobertura de pruebas en GitHub Pages | `coverage/index.html`, `coverage/coverage.xml` | Done |
| Publicar pruebas BDD en GitHub Pages | `bdd/index.html`, `bdd/report.json` | Done |
| Publicar pruebas de interfaz con Playwright | `ui-tests/index.html`, capturas y videos | Done |
| Publicar reporte de mutacion | `mutation/index.html`, `mutation/results.txt`, `mutation/run.log` | Done |
| Publicar Semgrep y Snyk en GitHub Pages | `semgrep/index.html`, `snyk/dependencies.html`, `snyk/code.html` | Done |
| Configurar SonarCloud | `sonar-project.properties`, `.github/workflows/static-analysis.yml` | Done tecnico / pendiente token |
| Agregar anotaciones en GitHub Actions | `scripts/emit_github_annotations.py` y workflows | Done |
| Documentar uso de SonarCloud | `docs/QA_ANALISIS_ESTATICO.md` | Done |

## Como actualizar el GitHub Project

1. Entrar al proyecto de la organizacion o del aula.
2. Crear o ubicar cada item de la tabla anterior.
3. Vincular cada item con su commit, workflow o URL de GitHub Pages.
4. Cambiar el campo `Status` a `Done`.
5. Si se pide responsable, asignar al integrante que hizo la tarea o al equipo completo.

## Evidencias rapidas

Portal QA:

```text
https://upt-faing-epis.github.io/proyecto-si784-2026-i-u3-ids-sistema-deteccion-de-instrusos_u3/
```

Workflow principal:

```text
Deploy QA Portal to GitHub Pages
```

Workflow de analisis:

```text
Static Analysis
```
