"""POST validation test for agregar-dominio (requires logged-in client with active plan)."""
import re
import sys

import requests

BASE = "http://localhost:8000"
LOGIN_URL = f"{BASE}/Clientes/login/"
VALIDATE_URL = f"{BASE}/dominios/agregar-dominio/"


def extract_csrf(html: str) -> str:
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
    return match.group(1) if match else ""


def login(session: requests.Session, username: str, password: str) -> bool:
    login_page = session.get(LOGIN_URL)
    csrf = extract_csrf(login_page.text)
    response = session.post(
        LOGIN_URL,
        data={
            "csrfmiddlewaretoken": csrf,
            "username": username,
            "password": password,
        },
        headers={"Referer": LOGIN_URL},
    )
    return response.status_code in (200, 302)


def validate_domain(session: requests.Session, domain: str) -> str:
    page = session.get(VALIDATE_URL)
    csrf = extract_csrf(page.text)
    response = session.post(
        VALIDATE_URL,
        data={
            "csrfmiddlewaretoken": csrf,
            "dominio": domain,
            "accion": "validar",
        },
        headers={"Referer": VALIDATE_URL},
    )
    return response.text


def classify(html: str) -> str:
    lower = html.lower()
    if "dominio disponible" in lower or "disponible y listo" in lower:
        return "available"
    if "no tiene web activa" in lower or "está protegido" in lower:
        return "old_protected_bug"
    if "en uso" in lower or "no disponible" in lower or "ya está registrado" in lower:
        return "taken"
    if "no se pudo verificar" in lower:
        return "error"
    return "unknown"


def main() -> int:
    username = sys.argv[1] if len(sys.argv) > 1 else ""
    password = sys.argv[2] if len(sys.argv) > 2 else ""
    if not username:
        print("Usage: python test_agregar_dominio_validate.py <username> <password>")
        return 2

    session = requests.Session()
    if not login(session, username, password):
        print("FAIL: could not log in")
        return 1

    cases = [
        ("eo-test-xyz12345.com", "available"),
        ("google.com", "taken"),
    ]
    failed = 0
    for domain, expected in cases:
        html = validate_domain(session, domain)
        result = classify(html)
        ok = result == expected
        print(f"{'PASS' if ok else 'FAIL'} {domain}: got={result} expected={expected}")
        if not ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
