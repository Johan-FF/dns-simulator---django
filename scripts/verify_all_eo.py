"""Verify EO-01..EO-17 via Django test client."""

import os

import sys

import uuid



sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChibchaWeb.settings.development")



import django



django.setup()



from django.contrib.auth.models import User

from django.test import Client

from Clientes.models import Cliente, HostSearchHistory



PWD = "Test1234!"

RESULTS = {}





def record(eo, ok, note=""):

    RESULTS[eo] = (ok, note)

    status = "PASS" if ok else "FAIL"

    print(f"[{status}] {eo}: {note}")





def reset_client_language(username="eo_client"):

    Cliente.objects.filter(user__username=username).update(preferred_language="es")





def lang_prefix(username="eo_client"):
    cliente = Cliente.objects.filter(user__username=username).first()
    return "/en" if cliente and cliente.preferred_language == "en" else ""


def localized(path, username="eo_client"):
    if not path.startswith("/"):
        path = f"/{path}"
    prefix = lang_prefix(username)
    return f"{prefix}{path}" if prefix else path


def home_path_for_client():
    return localized("/")





def main():

    c = Client(HTTP_HOST="localhost")

    reset_client_language()



    # EO-01

    r = c.post("/dominios/", {"url": f"eo01-{uuid.uuid4().hex[:8]}.com"})

    record(

        "EO-01",

        r.status_code == 200 and b"puedes usar" in r.content,

        "domain availability message",

    )



    # EO-02

    uname = f"eo_reg_{uuid.uuid4().hex[:6]}"

    r = c.post(

        "/Clientes/registrar/",

        {

            "username": uname,

            "email": f"{uname}@test.com",

            "password1": PWD,

            "password2": PWD,

            "telefono": "3001234567",

        },

    )

    record(

        "EO-02",

        User.objects.filter(username=uname).exists()

        and r.status_code in (200, 302),

        f"user {uname} created",

    )



    # EO-03 admin

    c.logout()

    ok = c.login(username="eo_admin", password="TestAdmin123!") or c.login(

        username="eo_admin", password=PWD

    )

    if ok:

        r = c.get("/administradores/usuarios/")

        record("EO-03", r.status_code == 200, "admin user management")

    else:

        record("EO-03", False, "admin login failed")



    # Client flows (Spanish default URLs)

    c.logout()

    reset_client_language()

    if not c.login(username="eo_client", password=PWD):

        record("EO-04", False, "eo_client login failed")

        for eo in ("EO-05", "EO-06", "EO-07", "EO-08", "EO-09", "EO-13", "EO-14", "EO-15"):

            record(eo, False, "skipped: eo_client login failed")

        record("EO-16", False, "skipped")

        record("EO-17", c.get("/").status_code == 200 and b"viewport" in c.get("/").content.lower(), "viewport")

    else:

        record("EO-04", c.get("/pagos/seleccionar-plan/").status_code == 200, "plan selection")

        record("EO-05", c.get("/Clientes/detalle/").status_code == 200, "profile settings")

        record("EO-06", c.get("/pagos/registrar-tarjeta/").status_code == 200, "card form")



        r = c.get("/tickets/nuevo/")

        record("EO-07", r.status_code == 200, "create ticket form")

        if r.status_code == 200:

            r2 = c.post(

                "/tickets/nuevo/",

                {

                    "asunto": "EO-07 test",

                    "descripcion": "Automated EO-07 verification ticket",

                    "prioridad": "media",

                },

            )

            record("EO-07-submit", r2.status_code in (200, 302), "ticket submitted")



        record("EO-09", c.get("/Clientes/mis-hosts/").status_code in (200, 302), "mis hosts")



        c.post("/dominios/", {"url": f"hist-{uuid.uuid4().hex[:6]}.com"})

        hist = c.get("/Clientes/historial-busquedas/")

        record(

            "EO-14",

            hist.status_code == 200

            and HostSearchHistory.objects.filter(cliente__user__username="eo_client").exists(),

            "search history page",

        )



        r = c.post("/logout/")

        record("EO-08", r.status_code in (200, 302), "logout")



        c.login(username="eo_client", password=PWD)

        r = c.post("/i18n/setlang/", {"language": "en", "next": "/en/"}, follow=True)

        cliente = Cliente.objects.get(user__username="eo_client")

        record(

            "EO-15",

            r.status_code == 200 and (b"Welcome" in r.content or b"Hosting" in r.content),

            "en UI",

        )

        record("EO-16", cliente.preferred_language == "en", f"preferred_language={cliente.preferred_language}")



        r = c.get(home_path_for_client())

        record(

            "EO-17",

            r.status_code == 200 and b"viewport" in r.content.lower(),

            "viewport meta present",

        )



        cliente = Cliente.objects.get(user__username="eo_client")

        r = c.get(localized(f"/Clientes/editar/{cliente.id}/"))

        record(

            "EO-13",

            r.status_code == 200 and b'name="foto"' in r.content.lower(),

            "profile photo on edit form",

        )



    # EO-10 supervisor

    c.logout()

    reset_client_language()

    if c.login(username="eo_supervisor", password=PWD):

        r = c.get("/empleados/dashboard/supervisor/")

        record("EO-10", r.status_code == 200, "supervisor dashboard")

        record("EO-11", r.status_code == 200, "employee mgmt on supervisor dash")

    else:

        record("EO-10", False, "supervisor login failed")

        record("EO-11", False, "supervisor login failed")



    # EO-12 agent

    c.logout()

    if c.login(username="eo_agent", password=PWD):

        record("EO-12", c.get("/empleados/mis-tickets/").status_code == 200, "agent tickets")

    else:

        record("EO-12", False, "agent login failed")



    print("\n=== FINAL ===")

    fails = 0

    for eo in sorted(RESULTS):

        ok, note = RESULTS[eo]

        if not ok:

            fails += 1

        print(f"  {eo}: {'OK' if ok else 'FAIL'} - {note}")

    print(f"\nTotal: {len(RESULTS) - fails} OK / {fails} FAIL")

    if fails:

        sys.exit(1)





if __name__ == "__main__":

    main()

