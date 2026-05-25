"""Payment processing for plans and distributor page packages."""
import hashlib
import secrets

from django.conf import settings
from django.utils.translation import gettext as _

from Pagos.models import Pago, PagoDistribuidor, TarjetaCredito

from .subscription_service import SubscriptionService


class PaymentService:
    """Create payments and update related business state."""

    @staticmethod
    def tokenize_card_number(card_number: str) -> tuple[str, str]:
        """Return (last4, payment_token) without storing PAN or CVV."""
        digits = ''.join(c for c in card_number if c.isdigit())
        last4 = digits[-4:]
        token = hashlib.sha256(f'{digits}:{secrets.token_hex(8)}'.encode()).hexdigest()[:32]
        return last4, token

    @classmethod
    def register_card(cls, cliente, card_number: str, holder_name: str, expiry: str) -> TarjetaCredito:
        last4, payment_token = cls.tokenize_card_number(card_number)
        tarjeta = TarjetaCredito.objects.create(
            last4=last4,
            payment_token=payment_token,
            card_brand=TarjetaCredito.detect_brand(card_number),
            nombre_titular=holder_name.upper(),
            fecha_expiracion=expiry,
            cliente=cliente,
        )
        return tarjeta

    @classmethod
    def process_plan_payment(cls, cliente, plan: str, modality: str, direccion, tarjeta) -> Pago:
        monto = SubscriptionService.get_plan_price(plan, modality)
        pago = Pago.objects.create(
            cliente=cliente,
            direccion=direccion,
            tarjeta_usada=tarjeta,
            monto=monto,
        )
        SubscriptionService.activate_subscription(cliente, plan, modality)
        return pago

    @classmethod
    def process_distributor_package_payment(
        cls,
        cliente,
        cantidad_paginas: int,
        direccion,
        tarjeta,
    ) -> PagoDistribuidor:
        precio_unitario = settings.PRECIO_POR_PAGINA_DISTRIBUIDOR
        monto = cantidad_paginas * precio_unitario

        pago_dist = PagoDistribuidor.objects.create(
            cliente=cliente,
            direccion=direccion,
            tarjeta_usada=tarjeta,
            monto=monto,
            cantidad_paginas=cantidad_paginas,
            descripcion=_('Purchase of %(count)s pages for resale') % {'count': cantidad_paginas},
        )

        try:
            distribuidor_perfil = cliente.perfil_distribuidor
            distribuidor_perfil.cantidad_dominios += cantidad_paginas
            distribuidor_perfil.save(update_fields=['cantidad_dominios'])
        except Exception:
            pass

        return pago_dist
