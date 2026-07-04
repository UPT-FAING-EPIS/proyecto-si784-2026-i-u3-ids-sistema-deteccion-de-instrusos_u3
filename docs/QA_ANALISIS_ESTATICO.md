# Analisis estatico y SonarCloud

Este proyecto genera evidencia de analisis estatico desde GitHub Actions y la publica en GitHub Pages.

## Informe detallado Sonar / Semgrep / Snyk

El workflow `Deploy QA Portal to GitHub Pages` genera:

- `static-analysis/index.html`: resumen consolidado de SonarCloud, Semgrep y Snyk.
- `semgrep/index.html`: hallazgos SAST detectados por Semgrep.
- `snyk/dependencies.html`: vulnerabilidades de dependencias Python.
- `snyk/code.html`: hallazgos de Snyk Code si el token esta configurado.

Semgrep se ejecuta sin secreto. Snyk requiere registrar `SNYK_TOKEN` en:

```text
GitHub > Settings > Secrets and variables > Actions > New repository secret
```

## Escaneo en SonarCloud

El workflow `.github/workflows/static-analysis.yml` incluye el job `SonarQube Cloud`.

Para activarlo:

1. Crear o importar el proyecto en SonarCloud.
2. Confirmar que el proyecto use estos datos, o ajustar `sonar-project.properties`:

   ```text
   sonar.projectKey=UPT-FAING-EPIS_proyecto-si784-2026-i-u3-ids-sistema-deteccion-de-instrusos_u3
   sonar.organization=upt-faing-epis
   ```

3. Crear un token en SonarCloud.
4. Guardarlo en GitHub como secreto:

   ```text
   SONAR_TOKEN
   ```

5. Ejecutar el workflow `Static Analysis` o hacer push a `main`.

El escaneo genera `coverage.xml` con pytest-cov y lo envia a SonarCloud junto con el codigo de `src/`, `web/`, `main.py`, `run_dashboard.py` y `trafficwatch_desktop.py`.

## Evidencia esperada

En GitHub Actions debe verse el job:

```text
Static Analysis / SonarQube Cloud
```

En GitHub Pages debe verse:

```text
Analisis Estatico Detallado
Escaneo en SonarCloud
```
