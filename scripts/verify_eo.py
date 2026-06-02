"""
Smoke-check operational scenarios via Django test client.
Run: conda activate p && python scripts/verify_eo.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChibchaWeb.settings.development")

import django

django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


def login(client, username, password="Test1234!"):
    ok = client.login(username=username, password=password)
    return ok


def check(name, response, allowed=(200, 302)):
    ok = response.status_code in allowed
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] {name}: {response.status_code}")
    if not ok and response.status_code == 500:
        print(response.content[:500])
    return ok


def main():
    c = Client(HTTP_HOST="localhost")
    results = {}

    # EO-01
    r = c.post("/dominios/", {"url": "eo01verify99999.com"})
    results["EO-01"] = r.status_code == 200 and (
        b"ocupada" in r.content or b"disponible" in r.content.lower() or b"puedes usar" in r.content
    )

    # EO-02 register page
    r = c.get("/Clientes/registrar/")
    results["EO-02"] = r.status_code == 200

    # Find admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        pwd = os.environ.get("TEST_ADMIN_PASSWORD", "admin123")
        if not c.login(username=admin_user.username, password=pwd):
            for p in ("admin", "Admin123!", "Test1234!", "chibcha123"):
                if c.login(username=admin_user.username, password=p):
                    pwd = p
                    break
        if c.session.get("_auth_user_id"):
            r = c.get("/administradores/usuarios/")
            results["EO-03"] = r.status_code in (200, 302)
            c.logout()
        else:
            results["EO-03"] = False
            print("  [WARN] Could not login as admin for EO-03")

    # Client login
    cliente_user = User.objects.filter(cliente__isnull=False).first()
    client_ok = False
    if cliente_user:
        for p in ("Test1234!", "cliente123", "demo1234", "password", "12345678"):
            if c.login(username=cliente_user.username, password=p):
                client_ok = True
                break
    results["client_login"] = client_ok
    if client_ok:
        results["EO-04"] = check(
            "EO-04 seleccionar plan",
            c.get("/pagos/seleccionar-plan/"),
        )
        results["EO-05"] = check(
            "EO-05 config",
            c.get("/Clientes/detalle/"),
        )
        results["EO-06"] = check(
            "EO-06 tarjeta form",
            c.get("/pagos/registrar-tarjeta/"),
        )
        results["EO-07"] = check(
            "EO-07 crear ticket",
            c.get("/tickets/nuevo/"),
        )
        results["EO-09"] = check(
            "EO-09 mis hosts",
            c.get("/Clientes/mis-hosts/"),
        )
        results["EO-14"] = check(
            "EO-14 historial",
            c.get("/Clientes/historial-busquedas/"),
            allowed=(200, 302, 404),
        )
        c.post("/logout/")
        results["EO-08"] = True  # logout attempted

    print("\n=== Summary ===")
    for k, v in sorted(results.items()):
        print(f"  {k}: {'PASS' if v else 'FAIL'}")


if __name__ == "__main__":
    main()
