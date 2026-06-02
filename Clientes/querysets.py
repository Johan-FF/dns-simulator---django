"""Optimized query helpers for Cliente listings."""
from django.db.models import Count, Q

from Dominios.models import Dominios

from .models import Cliente


def clientes_with_domain_counts():
    """Annotate domain counts to avoid N+1 in list/detail views."""
    plan_domains = Count(
        'dominios',
        filter=Q(dominios__compraDistribuidor=False),
        distinct=True,
    )
    distributor_domains = Count(
        'dominios',
        filter=Q(dominios__compraDistribuidor=True),
        distinct=True,
    )
    total_domains = Count('dominios', distinct=True)
    return Cliente.objects.select_related('user').annotate(
        dominios_plan_count=plan_domains,
        _dominios_distribuidor_count=distributor_domains,
        dominios_total_count=total_domains,
    )


def attach_domain_counts(cliente):
    """Attach annotated counts to a single cliente instance if missing."""
    if hasattr(cliente, 'dominios_plan_count'):
        return cliente
    counts = Dominios.objects.filter(clienteId=cliente).aggregate(
        dominios_plan_count=Count('id', filter=Q(compraDistribuidor=False)),
        _dominios_distribuidor_count=Count('id', filter=Q(compraDistribuidor=True)),
        dominios_total_count=Count('id'),
    )
    for key, value in counts.items():
        setattr(cliente, key, value)
    return cliente
