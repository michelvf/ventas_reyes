# Generated by Django 5.2 on 2025-05-17 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0026_alter_cuenta_cien_pesos_alter_cuenta_cinco_pesos_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contador_billete",
            name="tipo_cuenta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tipos_cuentas",
                to="ventas.tipo_cuenta",
            ),
        ),
    ]
