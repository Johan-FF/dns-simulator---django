import pytest

from .performance_helpers import SIMPLE_THRESHOLD_SECONDS, seed_domains, timed_call, url_name


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_list_view_under_one_second(cliente_logueado, cliente_activo, performance_recorder):
    seed_domains(cliente_activo, total=120, prefix="qa-list")

    response, elapsed = timed_call(lambda: cliente_logueado.get(url_name("clientes:mis_hosts")))

    assert response.status_code != 500
    assert response.status_code == 200
    assert elapsed < SIMPLE_THRESHOLD_SECONDS
    assert "Mis Hosts" in response.content.decode(errors="ignore")

    performance_recorder(
        scenario="Listado de dominios del cliente",
        module="Clientes.mis_hosts",
        test_type="Vista HTTP con datos semilla bulk_create",
        elapsed_values=[elapsed],
        threshold="< 1.0 s y sin HTTP 500",
        result="APROBADO",
        evidence="Salida pytest y reporte de listado",
    )
