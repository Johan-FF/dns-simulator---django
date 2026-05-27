import pytest

from Dominios.models import Dominios

from .performance_helpers import SIMPLE_THRESHOLD_SECONDS, seed_domains, timed_call


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_search_filter_orm_under_one_second(cliente_activo, performance_recorder):
    # TODO: completar URL/vista de búsqueda o filtro de dominios cuando el módulo la exponga.
    seed_domains(cliente_activo, total=200, prefix="qa-search")
    seed_domains(cliente_activo, total=50, prefix="otro", compra_distribuidor=True)

    results, elapsed = timed_call(
        lambda: list(
            Dominios.objects.filter(
                clienteId=cliente_activo,
                nombreDominio__icontains="qa-search",
                compraDistribuidor=False,
            ).order_by("nombreDominio")[:25]
        )
    )

    assert len(results) == 25
    assert elapsed < SIMPLE_THRESHOLD_SECONDS

    performance_recorder(
        scenario="Búsqueda/filtro de dominios",
        module="Dominios ORM/SQLite",
        test_type="Capa de datos por ausencia de URL/vista",
        elapsed_values=[elapsed],
        threshold="< 1.0 s",
        result="APROBADO CON TODO",
        evidence="Consulta ORM filtrada por nombre y compraDistribuidor",
        notes="TODO: implementar vista/URL de búsqueda o filtro para validar flujo HTTP.",
    )
