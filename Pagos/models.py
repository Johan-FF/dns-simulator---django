from django.db import models
from Clientes.models import Cliente
from django.utils import timezone
from .validators import validar_tarjeta,VALIDADORES_DIRECCIONES

class Pais(models.Model):
    paisId = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Paises"
        verbose_name = "Pais"

class Direccion(models.Model):
    direccionId = models.AutoField(primary_key=True, unique=True)
    ubicacion = models.CharField(max_length=50)
    codigoPostal = models.CharField(max_length=10)
    
    # Relación con el país de esta dirección
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    
    # Relación con el cliente (que a su vez está vinculado al User)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='direcciones')

    def clean(self):
        """Valida la ubicación usando una función por país (si existe)."""
        super().clean()
        validador = VALIDADORES_DIRECCIONES.get(self.pais.nombre.lower())
        if validador:
            validador(self.ubicacion)

    def __str__(self):
        return f"{self.ubicacion}, {self.codigoPostal}, {self.pais}"

class TarjetaCredito(models.Model):
    """Stores only tokenized/mock payment reference — never full PAN or CVV."""

    last4 = models.CharField(max_length=4)
    payment_token = models.CharField(max_length=64, unique=True)
    card_brand = models.CharField(max_length=20, blank=True)
    nombre_titular = models.CharField(max_length=50)
    fecha_expiracion = models.CharField(max_length=5)  # MM/YY format

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tarjetas')

    @staticmethod
    def detect_brand(card_number: str) -> str:
        digits = ''.join(c for c in card_number if c.isdigit())
        if digits.startswith('4'):
            return 'VISA'
        if digits.startswith(('51', '52', '53', '54', '55')) or digits[:2] in {f'{i}' for i in range(22, 28)}:
            return 'MasterCard'
        if digits.startswith(('300', '301', '302', '303', '304', '305')) or digits[:2] in ('36', '38', '39'):
            return 'Diners Club'
        return 'Unknown'

    def __str__(self):
        return f"**** **** **** {self.last4}"

    @property
    def masked_display(self):
        return f"**** **** **** {self.last4}"
    

class Pago(models.Model):
    
    pagoId = models.AutoField(primary_key=True, unique=True)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos')
    
    tarjeta_usada = models.ForeignKey(
        TarjetaCredito,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos_realizados',
        verbose_name="Tarjeta utilizada"
    )
    
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pago de ${self.monto} por {self.cliente.user.username} el {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class PagoDistribuidor(Pago):
    cantidad_paginas = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=255, blank=True, help_text="Detalle opcional de la compra (ej: 'paquete de 100 páginas')")