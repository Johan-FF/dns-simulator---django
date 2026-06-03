import pytest
from unittest.mock import MagicMock

from Dominios.domain_availability import (
    DomainRegistrationStatus,
    check_domain_registration,
)


@pytest.mark.parametrize(
    "status_code,expected_status",
    [
        (404, DomainRegistrationStatus.AVAILABLE),
        (200, DomainRegistrationStatus.REGISTERED),
    ],
)
def test_check_domain_registration_rdap_com(monkeypatch, status_code, expected_status):
    mock_response = MagicMock(status_code=status_code)

    def fake_get(url, timeout=None, headers=None):
        assert "verisign.com" in url
        return mock_response

    monkeypatch.setattr(
        "Dominios.domain_availability.requests.get",
        fake_get,
    )
    if expected_status == DomainRegistrationStatus.REGISTERED:
        monkeypatch.setattr(
            "Dominios.domain_availability._has_active_website",
            lambda _domain: False,
        )

    result = check_domain_registration("example-domain-xyz.com")

    assert result.status == expected_status


def test_check_domain_registration_dns_fallback_when_rdap_fails(monkeypatch):
    def fake_get(*args, **kwargs):
        raise ConnectionError("rdap unavailable")

    monkeypatch.setattr(
        "Dominios.domain_availability.requests.get",
        fake_get,
    )
    monkeypatch.setattr(
        "Dominios.domain_availability._domain_resolves_in_dns",
        lambda _domain: False,
    )

    result = check_domain_registration("eo-test-xyz12345.com")

    assert result.status == DomainRegistrationStatus.AVAILABLE
