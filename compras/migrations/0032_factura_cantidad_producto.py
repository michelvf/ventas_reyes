# Generated by Django 5.2 on 2025-06-13 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0031_alter_detallefactura_cantidad_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="factura",
            name="cantidad_producto",
            field=models.IntegerField(default=0),
        ),
    ]
