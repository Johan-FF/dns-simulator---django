"""Forms for payment-related views."""
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Direccion, Pais, TarjetaCredito
from .validators import VALIDADORES_DIRECCIONES, validar_tarjeta


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['ubicacion', 'codigoPostal', 'pais']
        labels = {
            'ubicacion': _('Address'),
            'codigoPostal': _('Postal code'),
            'pais': _('Country'),
        }

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data['ubicacion']
        pais = self.cleaned_data.get('pais')
        if pais:
            validador = VALIDADORES_DIRECCIONES.get(pais.nombre.lower())
            if validador:
                validador(ubicacion)
        return ubicacion


class TarjetaCreditoForm(forms.Form):
    numero = forms.CharField(
        max_length=19,
        label=_('Card number'),
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}),
    )
    nombre_titular = forms.CharField(max_length=50, label=_('Cardholder name'))
    fecha_expiracion = forms.CharField(max_length=5, label=_('Expiry (MM/YY)'))
    cvv = forms.CharField(
        max_length=4,
        label=_('CVV'),
        widget=forms.PasswordInput,
        help_text=_('Used only for validation; never stored.'),
    )

    def clean_numero(self):
        numero = self.cleaned_data['numero'].replace(' ', '')
        validar_tarjeta(numero)
        return numero

    def clean_fecha_expiracion(self):
        fecha = self.cleaned_data['fecha_expiracion']
        if not re.match(r'^\d{2}/\d{2}$', fecha):
            raise ValidationError(_('Expiry must be in MM/YY format.'))
        return fecha

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not re.match(r'^\d{3,4}$', cvv):
            raise ValidationError(_('CVV must be 3 or 4 digits.'))
        return cvv


class PlanSelectionForm(forms.Form):
    plan = forms.ChoiceField(label=_('Plan'))
    modalidad = forms.ChoiceField(
        label=_('Billing period'),
        choices=[
            ('mensual', _('Monthly')),
            ('semestral', _('Semi-annual')),
            ('anual', _('Annual')),
        ],
    )

    def __init__(self, *args, plan_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if plan_choices:
            self.fields['plan'].choices = plan_choices


class PaymentSelectionForm(forms.Form):
    direccion_id = forms.IntegerField()
    tarjeta_id = forms.IntegerField()


class PaqueteSelectionForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, max_value=1000, initial=1)
