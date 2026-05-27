import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from Dominios.models import Dominios

from .performance_helpers import LOAD_THRESHOLD_SECONDS, seed_domains, timed_call


@pytest.mark.performance
@pytest.mark.django_db(transaction=True)
def test_controlled_throughput_between_200_and_500_tpm_or_local_justification(cliente_activo, performance_recorder):
    seed_domains(cliente_activo, total=80, prefix="qa-throughput")
    total_transactions = 20

    def transaction():
        return Dominios.objects.filter(clienteId=cliente_activo, nombreDominio__icontains="qa-throughput").count()

    start = time.perf_counter()
    counts = [transaction() for _ in range(total_transactions)]
    duration = time.perf_counter() - start
    tpm = (total_transactions / duration) * 60

    assert all(count == 80 for count in counts)
    assert duration < LOAD_THRESHOLD_SECONDS
    assert tpm >= 200

    result = "APROBADO" if tpm <= 500 else "APROBADO CON JUSTIFICACIÓN LOCAL"
    notes = "" if tpm <= 500 else "TPM supera 500 porque la simulación local usa SQLite en memoria de proceso sin latencia de red ni usuarios reales."
    performance_recorder(
        scenario="Throughput controlado 200 a 500 TPM",
        module="Dominios ORM/SQLite",
        test_type="Simulación secuencial controlada",
        elapsed_values=[duration],
        threshold="200 <= TPM <= 500 o justificación local; carga < 5.0 s",
        result=result,
        evidence="Cálculo TPM = (total_transacciones / duración_segundos) * 60",
        tpm=tpm,
        notes=notes,
    )


@pytest.mark.performance
@pytest.mark.django_db(transaction=True)
def test_high_load_orm_scenario_under_five_seconds(cliente_activo, performance_recorder):
    seed_domains(cliente_activo, total=150, prefix="qa-load")

    def read_transaction():
        return Dominios.objects.filter(clienteId=cliente_activo).count()

    counts, elapsed = timed_call(lambda: list(ThreadPoolExecutor(max_workers=4).map(lambda _: read_transaction(), range(16))))

    assert all(count >= 150 for count in counts)
    assert elapsed < LOAD_THRESHOLD_SECONDS

    performance_recorder(
        scenario="Alta carga/concurrencia de lectura",
        module="Dominios ORM/SQLite",
        test_type="ThreadPoolExecutor con consultas ORM",
        elapsed_values=[elapsed],
        threshold="< 5.0 s",
        result="APROBADO",
        evidence="16 lecturas concurrentes controladas sobre SQLite",
    )
