# Generated by Django 5.1.3 on 2024-12-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0004_alter_producto_imagen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="producto",
            name="imagen",
            field=models.ImageField(
                blank=True, null=True, upload_to="productos_compras/"
            ),
        ),
    ]
