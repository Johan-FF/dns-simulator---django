# Generated manually after changing phone numbers to text.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0006_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
