import pytest
import requests
import socket

from .performance_helpers import SIMPLE_THRESHOLD_SECONDS, timed_call, url_name


@pytest.mark.performance
@pytest.mark.django_db
def test_domain_availability_view_under_one_second(client, monkeypatch, performance_recorder):
    monkeypatch.setattr(socket, "gethostbyname", lambda domain: (_ for _ in ()).throw(OSError()))

    def raise_connection_error(*args, **kwargs):
        raise requests.RequestException("red simulada para prueba local")

    monkeypatch.setattr("Dominios.views.requests.get", raise_connection_error)
    client.get(url_name("dominios:verificar_url"))

    response, elapsed = timed_call(
        lambda: client.post(url_name("dominios:verificar_url"), {"url": "qa-disponible.test"})
    )

    assert response.status_code != 500
    assert elapsed < SIMPLE_THRESHOLD_SECONDS
    assert "qa-disponible.test" in response.content.decode(errors="ignore")

    performance_recorder(
        scenario="Consulta de disponibilidad de dominio",
        module="Dominios.verificar_url",
        test_type="Vista HTTP con Django Test Client",
        elapsed_values=[elapsed],
        threshold="< 1.0 s y sin HTTP 500",
        result="APROBADO",
        evidence="Salida pytest y fila de reporte de disponibilidad",
    )
