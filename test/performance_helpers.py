import time
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from Clientes.models import Cliente
from Dominios.models import Dominios


SIMPLE_THRESHOLD_SECONDS = 1.0
COMPLEX_THRESHOLD_SECONDS = 3.0
LOAD_THRESHOLD_SECONDS = 5.0


@pytest.fixture
def cliente_activo(db):
    user = User.objects.create_user(
        username=f"qa_cliente_{time.perf_counter_ns()}",
        password="TestPassword123",
        email="qa@example.test",
    )
    return Cliente.objects.create(
        user=user,
        telefono=3001234567,
        tiene_suscripcion=True,
        plan="Oro",
        fecha_inicio_suscripcion=timezone.now() - timedelta(days=1),
        fecha_fin_suscripcion=timezone.now() + timedelta(days=30),
    )


@pytest.fixture
def cliente_logueado(client, cliente_activo):
    client.force_login(cliente_activo.user)
    return client


def seed_domains(cliente, total=100, prefix="qa-domain", compra_distribuidor=False):
    domains = [
        Dominios(
            clienteId=cliente,
            nombreDominio=f"{prefix}-{index}-{time.perf_counter_ns()}.test",
            compraDistribuidor=compra_distribuidor,
        )
        for index in range(total)
    ]
    return Dominios.objects.bulk_create(domains)


def timed_call(callable_obj):
    start = time.perf_counter()
    result = callable_obj()
    elapsed = time.perf_counter() - start
    return result, elapsed


def url_name(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)
