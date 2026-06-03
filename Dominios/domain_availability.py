"""
Domain registration availability checks (RDAP with DNS fallback).
"""
from __future__ import annotations

import socket
from dataclasses import dataclass
from enum import Enum

import requests
from django.conf import settings

DEFAULT_RDAP_TIMEOUT = 8
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
)


class DomainRegistrationStatus(str, Enum):
    AVAILABLE = "available"
    REGISTERED = "registered"
    ERROR = "error"


@dataclass(frozen=True)
class DomainAvailabilityResult:
    status: DomainRegistrationStatus
    message: str
    web_active: bool = False

    @property
    def is_available(self) -> bool:
        return self.status == DomainRegistrationStatus.AVAILABLE


def _rdap_timeout() -> int:
    return int(getattr(settings, "DOMAIN_AVAILABILITY_RDAP_TIMEOUT", DEFAULT_RDAP_TIMEOUT))


def _rdap_headers() -> dict[str, str]:
    return {
        "Accept": "application/rdap+json",
        "User-Agent": "ChibchaWeb-DomainCheck/1.0",
    }


def _rdap_lookup_url(domain: str) -> str | None:
    domain = domain.lower().strip()
    if "." not in domain:
        return None
    tld = domain.rsplit(".", 1)[-1]
    if tld in ("com", "net"):
        return f"https://rdap.verisign.com/{tld}/v1/domain/{domain}"
    return f"https://rdap.org/domain/{domain}"


def _domain_resolves_in_dns(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except OSError:
        return False


def _has_active_website(domain: str) -> bool:
    try:
        response = requests.get(
            f"https://{domain}",
            timeout=3,
            headers={"User-Agent": BROWSER_USER_AGENT},
            allow_redirects=True,
        )
        return response.status_code < 400
    except requests.RequestException:
        return False


def _result_from_rdap_status(domain: str, status_code: int) -> DomainAvailabilityResult | None:
    if status_code == 404:
        return DomainAvailabilityResult(
            DomainRegistrationStatus.AVAILABLE,
            f"The domain '{domain}' is available for registration.",
        )
    if status_code == 200:
        web_active = _has_active_website(domain)
        if web_active:
            message = (
                f"The domain '{domain}' is registered and has an active website."
            )
        else:
            message = (
                f"The domain '{domain}' is already registered "
                f"(no active public website detected)."
            )
        return DomainAvailabilityResult(
            DomainRegistrationStatus.REGISTERED,
            message,
            web_active=web_active,
        )
    return None


def _dns_fallback(domain: str) -> DomainAvailabilityResult:
    if _domain_resolves_in_dns(domain):
        web_active = _has_active_website(domain)
        return DomainAvailabilityResult(
            DomainRegistrationStatus.REGISTERED,
            (
                f"The domain '{domain}' resolves in DNS and is likely already registered. "
                f"Registration lookup was inconclusive."
            ),
            web_active=web_active,
        )
    return DomainAvailabilityResult(
        DomainRegistrationStatus.AVAILABLE,
        (
            f"The domain '{domain}' appears available for registration "
            f"(registration lookup was inconclusive)."
        ),
    )


def check_domain_registration(domain: str) -> DomainAvailabilityResult:
    """
    Determine whether a domain name is available for registration.
    Uses RDAP when possible; falls back to DNS when RDAP is unreachable.
    """
    lookup_url = _rdap_lookup_url(domain)
    if not lookup_url:
        return DomainAvailabilityResult(
            DomainRegistrationStatus.ERROR,
            "Invalid domain format.",
        )

    try:
        response = requests.get(
            lookup_url,
            timeout=_rdap_timeout(),
            headers=_rdap_headers(),
        )
        rdap_result = _result_from_rdap_status(domain, response.status_code)
        if rdap_result is not None:
            return rdap_result
    except requests.RequestException:
        pass

    return _dns_fallback(domain)
