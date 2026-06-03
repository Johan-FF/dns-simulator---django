import pytest
from django.urls import reverse

from Dominios.models import Dominios

from .performance_helpers import cliente_activo, cliente_logueado


@pytest.mark.django_db
def test_configurar_dominio_page_for_owner(cliente_logueado, cliente_activo):
    dominio = Dominios.objects.create(
        clienteId=cliente_activo,
        nombreDominio="ejemplo-configurar.test",
    )
    url = reverse("dominios:configurar_dominio", kwargs={"dominio_id": dominio.id})
    response = cliente_logueado.get(url)
    assert response.status_code == 200
    assert b"ejemplo-configurar.test" in response.content


@pytest.mark.django_db
def test_configurar_dominio_denied_for_other_client(cliente_logueado, cliente_activo, db):
    from django.contrib.auth.models import User
    from Clientes.models import Cliente

    other_user = User.objects.create_user(
        username="other_host_client",
        password="TestPassword123",
    )
    other_cliente = Cliente.objects.create(user=other_user)
    dominio = Dominios.objects.create(
        clienteId=other_cliente,
        nombreDominio="otro-cliente.test",
    )
    url = reverse("dominios:configurar_dominio", kwargs={"dominio_id": dominio.id})
    response = cliente_logueado.get(url)
    assert response.status_code == 302
