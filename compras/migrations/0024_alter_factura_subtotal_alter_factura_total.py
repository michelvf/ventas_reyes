# Generated by Django 5.2 on 2025-05-29 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0023_alter_detallefactura_subtotal_alter_factura_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='factura',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
