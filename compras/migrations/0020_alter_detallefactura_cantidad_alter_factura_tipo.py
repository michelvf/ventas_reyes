# Generated by Django 5.2 on 2025-05-31 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0019_factura_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detallefactura",
            name="cantidad",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AlterField(
            model_name="factura",
            name="tipo",
            field=models.CharField(
                choices=[("c", "Compra"), ("v", "Venta")], default="c", max_length=1
            ),
        ),
    ]
