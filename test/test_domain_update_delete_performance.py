import pytest

from Dominios.models import Dominios

from .performance_helpers import COMPLEX_THRESHOLD_SECONDS, seed_domains, timed_call, url_name


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_update_orm_under_three_seconds(cliente_activo, performance_recorder):
    # TODO: completar URL/vista de actualización de dominios cuando el módulo la exponga.
    domain = seed_domains(cliente_activo, total=1, prefix="qa-update")[0]

    updated, elapsed = timed_call(
        lambda: Dominios.objects.filter(pk=domain.pk).update(nombreDominio="qa-updated-domain.test")
    )

    assert updated == 1
    assert elapsed < COMPLEX_THRESHOLD_SECONDS
    assert Dominios.objects.filter(pk=domain.pk, nombreDominio="qa-updated-domain.test").exists()

    performance_recorder(
        scenario="Actualización de dominio",
        module="Dominios ORM/SQLite",
        test_type="Capa de datos por ausencia de URL/vista",
        elapsed_values=[elapsed],
        threshold="< 3.0 s",
        result="APROBADO CON TODO",
        evidence="UPDATE ORM sobre nombreDominio",
        notes="TODO: implementar vista/URL de actualización para validar flujo HTTP.",
    )


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_delete_view_under_three_seconds(cliente_logueado, cliente_activo, performance_recorder):
    domain = seed_domains(cliente_activo, total=1, prefix="qa-delete")[0]

    response, elapsed = timed_call(
        lambda: cliente_logueado.post(url_name("dominios:eliminar_dominio", domain.id))
    )

    assert response.status_code != 500
    assert response.status_code in (302, 303)
    assert elapsed < COMPLEX_THRESHOLD_SECONDS
    assert not Dominios.objects.filter(pk=domain.pk).exists()

    performance_recorder(
        scenario="Eliminación de dominio",
        module="Dominios.eliminar_dominio",
        test_type="Vista HTTP con Django Test Client",
        elapsed_values=[elapsed],
        threshold="< 3.0 s y sin HTTP 500",
        result="APROBADO",
        evidence="POST eliminar_dominio con borrado ORM verificado",
    )
