"""Verify domain availability logic inside Docker (manage.py shell style)."""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChibchaWeb.settings")
django.setup()

from Dominios.domain_availability import check_domain_registration  # noqa: E402


def check(label: str, domain: str, expect_available: bool) -> None:
    result = check_domain_registration(domain)
    ok = result.is_available == expect_available
    status = "PASS" if ok else "FAIL"
    print(
        f"{status} {label}: {domain} -> {result.status.value} "
        f"(available={result.is_available}, web={result.web_active})"
    )
    if not ok:
        print(f"       message: {result.message}")


if __name__ == "__main__":
    check("random unregistered", "eo-test-xyz12345.com", expect_available=True)
    check("known registered", "google.com", expect_available=False)
