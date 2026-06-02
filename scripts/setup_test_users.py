"""Ensure EO test users exist with known passwords."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChibchaWeb.settings.development")

import django

django.setup()

from django.contrib.auth.models import User
from Clientes.models import Cliente
from Empleados.models import Empleado
from Administradores.models import Administrador

PWD = "Test1234!"


def ensure_user(username, email, **user_kwargs):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, **user_kwargs},
    )
    if created or not user.check_password(PWD):
        user.set_password(PWD)
        user.save()
    return user


def main():
    admin = ensure_user("eo_admin", "eo_admin@test.com", is_staff=True, is_superuser=True)
    Administrador.objects.get_or_create(
        user=admin,
        defaults={
            "activo": True,
            "puede_gestionar_usuarios": True,
            "puede_ver_estadisticas": True,
            "puede_gestionar_pagos": True,
        },
    )

    client = ensure_user("eo_client", "eo_client@test.com", first_name="EO", last_name="Client")
    cliente, _ = Cliente.objects.get_or_create(user=client)
    cliente.tiene_suscripcion = False
    cliente.plan = None
    cliente.preferred_language = "es"
    cliente.save()

    supervisor = ensure_user("eo_supervisor", "eo_supervisor@test.com", first_name="EO", last_name="Supervisor")
    Empleado.objects.get_or_create(
        user=supervisor,
        defaults={"rol": "supervisor", "nivel": 2, "activo": True, "telefono": 300123456},
    )

    agent = ensure_user("eo_agent", "eo_agent@test.com", first_name="EO", last_name="Agent")
    Empleado.objects.get_or_create(
        user=agent,
        defaults={"rol": "agente", "nivel": 1, "activo": True, "telefono": 300123457},
    )

    print("Test users ready (password: Test1234!)")
    print("  eo_admin, eo_client, eo_supervisor, eo_agent")


if __name__ == "__main__":
    main()
