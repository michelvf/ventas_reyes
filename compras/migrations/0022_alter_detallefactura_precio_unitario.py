# Generated by Django 5.2 on 2025-05-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0021_alter_detallefactura_precio_unitario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallefactura',
            name='precio_unitario',
            field=models.FloatField(),
        ),
    ]
