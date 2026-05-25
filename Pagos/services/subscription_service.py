"""Subscription activation logic centralized from views."""
from datetime import timedelta

from django.utils import timezone

from ChibchaWeb.planes import PLANES_DISPONIBLES


class SubscriptionService:
    """Activate or extend client hosting subscriptions."""

    MODALITY_DAYS = {
        'mensual': 30,
        'semestral': 180,
        'anual': 365,
    }

    @classmethod
    def get_plan_price(cls, plan_name: str, modality: str) -> float:
        if plan_name not in PLANES_DISPONIBLES:
            raise ValueError(f'Unknown plan: {plan_name}')
        key = f'precio_{modality}'
        if key not in PLANES_DISPONIBLES[plan_name]:
            raise ValueError(f'Unknown modality: {modality}')
        return PLANES_DISPONIBLES[plan_name][key]

    @classmethod
    def activate_subscription(cls, cliente, plan_name: str, modality: str) -> None:
        days = cls.MODALITY_DAYS.get(modality)
        if days is None:
            raise ValueError(f'Unknown modality: {modality}')

        now = timezone.now()
        cliente.tiene_suscripcion = True
        cliente.plan = plan_name
        cliente.fecha_inicio_suscripcion = now
        cliente.fecha_fin_suscripcion = now + timedelta(days=days)
        cliente.save(
            update_fields=[
                'tiene_suscripcion',
                'plan',
                'fecha_inicio_suscripcion',
                'fecha_fin_suscripcion',
            ]
        )
