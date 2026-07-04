from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree


def emit(level: str, title: str, message: str) -> None:
    safe_title = title.replace("\n", " ").replace(":", "-")
    safe_message = message.replace("\n", " ")
    print(f"::{level} title={safe_title}::{safe_message}")


def annotate_coverage(path: Path) -> int:
    if not path.exists():
        emit("warning", "Cobertura no disponible", f"No se encontro {path}")
        return 0

    try:
        root = ElementTree.fromstring(path.read_text(encoding="utf-8", errors="replace"))
    except ElementTree.ParseError as error:
        emit("warning", "Cobertura no legible", str(error))
        return 0

    line_rate = float(root.attrib.get("line-rate", 0)) * 100
    branch_rate = float(root.attrib.get("branch-rate", 0)) * 100
    lines_valid = root.attrib.get("lines-valid", "0")
    lines_covered = root.attrib.get("lines-covered", "0")
    message = (
        f"Cobertura total {line_rate:.2f}% "
        f"({lines_covered}/{lines_valid} lineas), ramas {branch_rate:.2f}%."
    )
    emit("notice", "Reporte de cobertura", message)
    if line_rate < 70:
        emit("warning", "Cobertura por debajo de 70%", message)
    return 0


def annotate_bdd(path: Path) -> int:
    if not path.exists():
        emit("warning", "BDD sin JSON", f"No se encontro {path}")
        return 0

    try:
        features = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError as error:
        emit("warning", "BDD JSON invalido", str(error))
        return 0

    total = passed = failed = skipped = 0
    for feature in features:
        for element in feature.get("elements", []):
            if element.get("type") != "scenario":
                continue
            total += 1
            statuses = [
                step.get("result", {}).get("status", "unknown")
                for step in element.get("steps", [])
            ]
            if any(status == "failed" for status in statuses):
                failed += 1
            elif statuses and all(status == "passed" for status in statuses):
                passed += 1
            else:
                skipped += 1

    message = f"Escenarios BDD: {total} total, {passed} aprobados, {failed} fallidos, {skipped} omitidos."
    emit("notice", "Reporte BDD", message)
    if failed:
        emit("error", "BDD con escenarios fallidos", message)
    return 0


def annotate_mutation(path: Path) -> int:
    if not path.exists():
        emit("warning", "Mutacion sin log", f"No se encontro {path}")
        return 0

    summary = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.search(
            r"(\d+)/(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)",
            line,
        )
        if match:
            summary = [int(value) for value in match.groups()]

    if not summary:
        emit("warning", "Mutacion sin resumen", "Mutmut no produjo un resumen numerico.")
        return 0

    checked, total, killed, no_tests, timeout, suspicious, survived, skipped = summary
    score = (killed / checked * 100) if checked else 0
    message = (
        f"Mutacion: {checked}/{total} evaluados, {killed} eliminados, "
        f"{survived} sobrevivientes, {score:.2f}% mutation score, "
        f"{no_tests} sin pruebas, {timeout} timeout, {suspicious} sospechosos, {skipped} omitidos."
    )
    emit("notice", "Reporte de mutacion", message)
    if survived:
        emit("warning", "Mutantes sobrevivientes", message)
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print("Uso: python scripts/emit_github_annotations.py coverage|bdd|mutation <archivo>")
        return 2

    report_type = sys.argv[1]
    path = Path(sys.argv[2])
    if report_type == "coverage":
        return annotate_coverage(path)
    if report_type == "bdd":
        return annotate_bdd(path)
    if report_type == "mutation":
        return annotate_mutation(path)

    print("Tipo invalido. Usa coverage, bdd o mutation.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
