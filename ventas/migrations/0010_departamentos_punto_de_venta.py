# Generated by Django 5.1.4 on 2025-01-13 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0009_fileupdate_actualizar"),
    ]

    operations = [
        migrations.AddField(
            model_name="departamentos",
            name="punto_de_venta",
            field=models.BooleanField(default=False),
        ),
    ]
