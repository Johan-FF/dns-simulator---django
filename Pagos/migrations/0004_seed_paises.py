from django.db import migrations


def seed_paises(apps, schema_editor):
    Pais = apps.get_model('Pagos', 'Pais')
    for nombre in ('Colombia', 'Ecuador', 'Peru'):
        Pais.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ('Pagos', '0003_secure_tarjeta_fields'),
    ]

    operations = [
        migrations.RunPython(seed_paises, migrations.RunPython.noop),
    ]
