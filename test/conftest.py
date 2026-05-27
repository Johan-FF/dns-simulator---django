import json
import os
from pathlib import Path
from statistics import mean

import django
import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChibchaWeb.settings")
django.setup()

pytest_plugins = ["tests.performance_helpers"]


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
JSON_REPORT = REPORTS_DIR / "performance_results.json"
MD_REPORT = REPORTS_DIR / "performance_results.md"


def pytest_configure(config):
    config._performance_metrics = []


@pytest.fixture
def performance_recorder(request):
    def record(
        *,
        scenario,
        module,
        test_type,
        elapsed_values,
        threshold,
        result,
        evidence,
        tpm=None,
        cpu=None,
        ram=None,
        size_mb=None,
        notes="",
    ):
        values = list(elapsed_values)
        metric = {
            "scenario": scenario,
            "module": module,
            "test_type": test_type,
            "average_seconds": round(mean(values), 6) if values else None,
            "max_seconds": round(max(values), 6) if values else None,
            "tpm": round(tpm, 2) if tpm is not None else None,
            "cpu_percent": round(cpu, 2) if cpu is not None else None,
            "ram_mb": round(ram, 2) if ram is not None else None,
            "size_mb": round(size_mb, 2) if size_mb is not None else None,
            "threshold": threshold,
            "result": result,
            "evidence": evidence,
            "notes": notes,
        }
        request.config._performance_metrics.append(metric)
        return metric

    return record


def pytest_sessionfinish(session, exitstatus):
    metrics = getattr(session.config, "_performance_metrics", [])
    REPORTS_DIR.mkdir(exist_ok=True)

    payload = {
        "project": "ChibchaWeb",
        "database": "SQLite",
        "tool": "pytest",
        "exitstatus": exitstatus,
        "metrics": metrics,
    }
    JSON_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Reporte parcial de pruebas de eficiencia - ChibchaWeb",
        "",
        "Ejecución generada por `python -m pytest -q` o por el intérprete Python disponible del entorno local.",
        "Base de datos: SQLite. No se modificaron modelos ni migraciones.",
        "",
        "| No. | Escenario | Módulo | Tipo de prueba | Tiempo promedio | Tiempo máximo | TPM | CPU/RAM | Umbral | Resultado | Evidencia sugerida |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for index, metric in enumerate(metrics, start=1):
        avg = _format_seconds(metric["average_seconds"])
        max_value = _format_seconds(metric["max_seconds"])
        tpm = "-" if metric["tpm"] is None else f"{metric['tpm']:.2f}"
        resource = _format_resource(metric)
        lines.append(
            "| {no} | {scenario} | {module} | {test_type} | {avg} | {max_value} | {tpm} | {resource} | {threshold} | {result} | {evidence} |".format(
                no=index,
                scenario=_escape(metric["scenario"]),
                module=_escape(metric["module"]),
                test_type=_escape(metric["test_type"]),
                avg=avg,
                max_value=max_value,
                tpm=tpm,
                resource=_escape(resource),
                threshold=_escape(metric["threshold"]),
                result=_escape(metric["result"]),
                evidence=_escape(metric["evidence"]),
            )
        )

    if not metrics:
        lines.append("| 1 | Sin métricas | pytest | sesión | - | - | - | - | - | SIN DATOS | Revisar salida de consola |")

    MD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _format_seconds(value):
    return "-" if value is None else f"{value:.6f} s"


def _format_resource(metric):
    parts = []
    if metric["cpu_percent"] is not None:
        parts.append(f"CPU {metric['cpu_percent']:.2f}%")
    if metric["ram_mb"] is not None:
        parts.append(f"RAM {metric['ram_mb']:.2f} MB")
    if metric["size_mb"] is not None:
        parts.append(f"Tamaño {metric['size_mb']:.2f} MB")
    return " / ".join(parts) if parts else "-"


def _escape(value):
    return str(value).replace("|", "\\|")
