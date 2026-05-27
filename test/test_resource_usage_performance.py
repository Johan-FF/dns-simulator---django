import os
import tempfile
import time
import zipfile
from pathlib import Path

import pytest

from Dominios.models import Dominios

from .performance_helpers import seed_domains


@pytest.mark.performance
@pytest.mark.django_db
def test_cpu_and_memory_usage_under_normal_load(cliente_activo, performance_recorder):
    psutil = pytest.importorskip("psutil", reason="Instalar con: pip install psutil")

    process = psutil.Process(os.getpid())
    seed_domains(cliente_activo, total=100, prefix="qa-resource")
    process.cpu_percent(interval=None)

    start = time.perf_counter()
    for _ in range(30):
        Dominios.objects.filter(clienteId=cliente_activo).count()
    elapsed = time.perf_counter() - start

    cpu_percent = process.cpu_percent(interval=0.1)
    ram_mb = process.memory_info().rss / (1024 * 1024)

    assert elapsed < 5.0
    assert cpu_percent <= 70.0
    assert ram_mb <= 1024.0

    result = "APROBADO" if ram_mb >= 512.0 else "APROBADO CON JUSTIFICACIÓN LOCAL"
    performance_recorder(
        scenario="Uso CPU/RAM bajo carga normal",
        module="Proceso pytest/Django",
        test_type="psutil sobre proceso local",
        elapsed_values=[elapsed],
        threshold="CPU <= 70%; RAM <= 1 GB; referencia acta 512 MB a 1 GB",
        result=result,
        evidence="Métrica psutil Process.cpu_percent y memory_info.rss",
        cpu=cpu_percent,
        ram=ram_mb,
        notes="RAM menor a 512 MB se justifica por ejecución local sin servidor WSGI permanente.",
    )


@pytest.mark.performance
def test_compressed_project_size_under_250_mb(performance_recorder):
    project_root = Path(__file__).resolve().parent.parent
    excluded_dirs = {".git", "venv", "__pycache__", ".pytest_cache", ".codex_pydeps"}
    max_size_mb = 250.0

    with tempfile.TemporaryDirectory() as tmpdir:
        archive_path = Path(tmpdir) / "chibchaweb-performance-size.zip"
        start = time.perf_counter()
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in project_root.rglob("*"):
                if path.is_dir():
                    continue
                if any(part in excluded_dirs for part in path.relative_to(project_root).parts):
                    continue
                archive.write(path, path.relative_to(project_root))
        elapsed = time.perf_counter() - start
        size_mb = archive_path.stat().st_size / (1024 * 1024)

    assert size_mb < max_size_mb

    performance_recorder(
        scenario="Tamaño del proyecto comprimido",
        module="Repositorio ChibchaWeb",
        test_type="ZIP temporal excluyendo .git, venv y cachés",
        elapsed_values=[elapsed],
        threshold="< 250 MB",
        result="APROBADO",
        evidence=f"Archivo temporal comprimido: {size_mb:.2f} MB",
        size_mb=size_mb,
        notes="ZIP temporal excluye dependencias locales de prueba y artefactos de control/caché.",
    )
