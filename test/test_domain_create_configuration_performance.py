import pytest

from Dominios.domain_availability import (
    DomainAvailabilityResult,
    DomainRegistrationStatus,
)
from Dominios.models import Dominios

from .performance_helpers import COMPLEX_THRESHOLD_SECONDS, timed_call, url_name


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_create_and_initial_configuration_under_three_seconds(
    cliente_logueado, cliente_activo, monkeypatch, performance_recorder
):
    monkeypatch.setattr(
        "Dominios.views.check_domain_registration",
        lambda _domain: DomainAvailabilityResult(
            DomainRegistrationStatus.AVAILABLE,
            "available for test",
        ),
    )
    monkeypatch.setattr("Dominios.views.EmailMessage.send", lambda self: 1)

    domain_name = "qa-create-config.test"
    response, elapsed = timed_call(
        lambda: cliente_logueado.post(
            url_name("dominios:agregar_dominio"),
            {"dominio": domain_name, "accion": "agregar"},
        )
    )

    assert response.status_code != 500
    assert response.status_code in (302, 303)
    assert elapsed < COMPLEX_THRESHOLD_SECONDS
    assert Dominios.objects.filter(clienteId=cliente_activo, nombreDominio=domain_name).exists()

    performance_recorder(
        scenario="Creación de dominio y configuración inicial",
        module="Dominios.agregar_dominio",
        test_type="Vista HTTP con red/correo simulados",
        elapsed_values=[elapsed],
        threshold="< 3.0 s y sin HTTP 500",
        result="APROBADO",
        evidence="POST agregar_dominio con creación ORM verificada",
    )
