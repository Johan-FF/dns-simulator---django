import hashlib
import secrets

from django.db import migrations, models


def migrate_card_data(apps, schema_editor):
    TarjetaCredito = apps.get_model('Pagos', 'TarjetaCredito')
    for tarjeta in TarjetaCredito.objects.all():
        old_numero = getattr(tarjeta, 'numero', '') or ''
        digits = ''.join(c for c in old_numero if c.isdigit())
        tarjeta.last4 = digits[-4:] if len(digits) >= 4 else '0000'
        tarjeta.payment_token = hashlib.sha256(
            f'{digits}:{tarjeta.pk}:{secrets.token_hex(8)}'.encode()
        ).hexdigest()[:32]
        if digits.startswith('4'):
            tarjeta.card_brand = 'VISA'
        elif digits.startswith(('51', '52', '53', '54', '55')):
            tarjeta.card_brand = 'MasterCard'
        else:
            tarjeta.card_brand = 'Unknown'
        tarjeta.save(update_fields=['last4', 'payment_token', 'card_brand'])


class Migration(migrations.Migration):

    dependencies = [
        ('Pagos', '0002_pagodistribuidor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjetacredito',
            name='last4',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='tarjetacredito',
            name='payment_token',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='tarjetacredito',
            name='card_brand',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.RunPython(migrate_card_data, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tarjetacredito',
            name='last4',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='tarjetacredito',
            name='payment_token',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.RemoveField(model_name='tarjetacredito', name='numero'),
        migrations.RemoveField(model_name='tarjetacredito', name='cvv'),
    ]
