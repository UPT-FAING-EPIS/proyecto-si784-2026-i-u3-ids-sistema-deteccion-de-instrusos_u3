from __future__ import annotations

import html
import re
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree


CSS = """
:root {
  color-scheme: light;
  --bg: #f6f8fb;
  --panel: #ffffff;
  --text: #172033;
  --muted: #5b6b84;
  --line: #d8e0ec;
  --accent: #0b83c5;
  --ok: #16803c;
  --warn: #9a6700;
  --bad: #b42318;
}
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Arial, Helvetica, sans-serif;
}
main {
  max-width: 1120px;
  margin: 0 auto;
  padding: 32px 20px 48px;
}
h1 {
  margin: 0 0 8px;
  color: #0f5f8f;
}
p {
  color: var(--muted);
  line-height: 1.55;
}
.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin: 24px 0;
}
.metric {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
}
.metric strong {
  display: block;
  font-size: 2rem;
  line-height: 1;
}
.passed, .killed {
  color: var(--ok);
}
.failed, .survived {
  color: var(--bad);
}
.skipped, .pending, .timeout, .suspicious {
  color: var(--warn);
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0 28px;
}
.button {
  display: inline-block;
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  font-weight: 700;
  padding: 10px 14px;
  text-decoration: none;
}
section {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 18px;
  margin-top: 16px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border-bottom: 1px solid var(--line);
  padding: 10px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #eef4fb;
}
.screenshots {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}
.screenshots img {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 6px;
}
pre {
  overflow: auto;
  background: #0f172a;
  color: #dbeafe;
  border-radius: 8px;
  padding: 14px;
  max-height: 560px;
}
"""


def write_page(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def parse_junit(path: Path) -> tuple[Counter, list[dict[str, str]]]:
    counts: Counter = Counter()
    rows: list[dict[str, str]] = []
    if not path.exists():
        return counts, rows

    try:
        root = ElementTree.fromstring(path.read_text(encoding="utf-8", errors="replace"))
    except ElementTree.ParseError:
        return counts, rows
    for case in root.iter("testcase"):
        status = "passed"
        if case.find("failure") is not None:
            status = "failed"
        elif case.find("error") is not None:
            status = "error"
        elif case.find("skipped") is not None:
            status = "skipped"

        counts[status] += 1
        rows.append(
            {
                "name": case.attrib.get("name", ""),
                "classname": case.attrib.get("classname", ""),
                "time": case.attrib.get("time", "0"),
                "status": status,
            }
        )

    return counts, rows


def render_test_report(
    title: str,
    description: str,
    junit_path: Path,
    raw_report_name: str,
    output_path: Path,
    screenshots_dir: Path | None = None,
) -> None:
    counts, rows = parse_junit(junit_path)
    total = sum(counts.values())
    passed = counts["passed"]
    failed = counts["failed"] + counts["error"]
    skipped = counts["skipped"]

    table_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['classname'])}</td>"
        f"<td>{html.escape(row['name'])}</td>"
        f"<td class='{html.escape(row['status'])}'>{html.escape(row['status'])}</td>"
        f"<td>{html.escape(row['time'])} s</td>"
        "</tr>"
        for row in rows
    ) or '<tr><td colspan="4">No se encontraron casos de prueba en el XML JUnit.</td></tr>'

    screenshots_html = ""
    if screenshots_dir and screenshots_dir.exists():
        images = sorted(screenshots_dir.glob("*.png"))
        if images:
            screenshots_html = """
<section>
  <h2>Evidencia visual</h2>
  <div class="screenshots">
""" + "\n".join(
                f'    <figure><img src="screenshots/{html.escape(image.name)}" alt="{html.escape(image.stem)}"><figcaption>{html.escape(image.stem)}</figcaption></figure>'
                for image in images
            ) + """
  </div>
</section>
"""

    status_text = "Aprobado" if failed == 0 and total > 0 else "Revisar"
    body = f"""
<h1>{html.escape(title)}</h1>
<p>{html.escape(description)}</p>
<div class="summary">
  <div class="metric"><strong>{total}</strong>Total</div>
  <div class="metric"><strong class="passed">{passed}</strong>Aprobadas</div>
  <div class="metric"><strong class="failed">{failed}</strong>Fallidas / errores</div>
  <div class="metric"><strong class="skipped">{skipped}</strong>Omitidas</div>
  <div class="metric"><strong>{status_text}</strong>Estado</div>
</div>
<div class="actions">
  <a class="button" href="{html.escape(raw_report_name)}">Ver reporte pytest-html</a>
</div>
<section>
  <h2>Casos ejecutados</h2>
  <table>
    <thead><tr><th>Modulo</th><th>Prueba</th><th>Resultado</th><th>Tiempo</th></tr></thead>
    <tbody>{table_rows}</tbody>
  </table>
</section>
{screenshots_html}
"""
    write_page(output_path, title, body)


def parse_mutmut_results(path: Path) -> tuple[Counter, list[tuple[str, str]]]:
    rows: list[tuple[str, str]] = []
    counts: Counter = Counter()
    if not path.exists():
        return counts, rows

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"\s*(.+?):\s*([a-zA-Z ]+)\s*$", line)
        if not match:
            continue
        mutant, status = match.groups()
        status = status.strip().lower().replace(" ", "_")
        counts[status] += 1
        rows.append((mutant.strip(), status))
    return counts, rows


def parse_mutmut_run_summary(path: Path) -> dict[str, int]:
    summary: dict[str, int] = {}
    if not path.exists():
        return summary

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.search(
            r"(\d+)/(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)",
            line,
        )
        if not match:
            continue
        checked, total, killed, no_tests, timeout, suspicious, survived, skipped = [
            int(value) for value in match.groups()
        ]
        if total >= checked:
            summary = {
                "checked": checked,
                "total": total,
                "killed": killed,
                "no_tests": no_tests,
                "timeout": timeout,
                "suspicious": suspicious,
                "survived": survived,
                "skipped": skipped,
            }
    return summary


def render_mutation_report(results_path: Path, output_path: Path, run_log_path: Path | None = None) -> None:
    counts, rows = parse_mutmut_results(results_path)
    summary = parse_mutmut_run_summary(run_log_path) if run_log_path else {}
    total = summary.get("total", sum(counts.values()))
    evaluated = summary.get("checked", total - counts["not_checked"])
    killed = summary.get("killed", counts["killed"])
    survived = summary.get("survived", counts["survived"])
    mutation_score = round((killed / evaluated) * 100, 2) if evaluated else 0
    pending = max(0, total - evaluated)

    rows_for_display = sorted(rows, key=lambda item: item[1] == "not_checked")
    sample_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(mutant)}</td>"
        f"<td class='{html.escape(status)}'>{html.escape(status.replace('_', ' '))}</td>"
        "</tr>"
        for mutant, status in rows_for_display[:120]
    ) or '<tr><td colspan="2">No se encontraron resultados de mutacion.</td></tr>'

    diagnostic = (
        "El reporte contiene mutantes evaluados por mutmut."
        if evaluated
        else "Mutmut genero mutantes, pero no llego a evaluarlos en esta ejecucion. Revisa tiempo de ejecucion o alcance configurado."
    )

    body = f"""
<h1>Pruebas de Mutacion</h1>
<p>Evaluacion de la calidad de las pruebas mediante mutantes generados sobre modulos criticos del IDS.</p>
<div class="summary">
  <div class="metric"><strong>{total}</strong>Mutantes generados</div>
  <div class="metric"><strong>{evaluated}</strong>Evaluados</div>
  <div class="metric"><strong class="killed">{killed}</strong>Eliminados</div>
  <div class="metric"><strong class="survived">{survived}</strong>Sobrevivientes</div>
  <div class="metric"><strong class="pending">{pending}</strong>Pendientes</div>
  <div class="metric"><strong>{mutation_score}%</strong>Mutation score</div>
</div>
<p>{html.escape(diagnostic)}</p>
<div class="actions">
  <a class="button" href="results.txt">Ver salida completa de mutmut</a>
  <a class="button" href="run.log">Ver log de ejecucion</a>
</div>
<section>
  <h2>Muestra de resultados</h2>
  <table>
    <thead><tr><th>Mutante</th><th>Estado</th></tr></thead>
    <tbody>{sample_rows}</tbody>
  </table>
</section>
"""
    write_page(output_path, "Pruebas de Mutacion - TrafficWatch IDS", body)


def main() -> None:
    report_type = None
    args = {}
    raw_args = iter(__import__("sys").argv[1:])
    for arg in raw_args:
        if arg == "--type":
            report_type = next(raw_args)
        elif arg.startswith("--"):
            args[arg[2:]] = next(raw_args)

    if report_type in {"unit", "ui"}:
        render_test_report(
            title=args["title"],
            description=args["description"],
            junit_path=Path(args["junit"]),
            raw_report_name=args["raw-report"],
            output_path=Path(args["output"]),
            screenshots_dir=Path(args["screenshots"]) if args.get("screenshots") else None,
        )
    elif report_type == "mutation":
        render_mutation_report(
            Path(args["results"]),
            Path(args["output"]),
            Path(args["run-log"]) if args.get("run-log") else None,
        )
    else:
        raise SystemExit("Uso: --type unit|ui|mutation ...")


if __name__ == "__main__":
    main()
