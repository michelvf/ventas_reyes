# Generated by Django 5.1.3 on 2024-12-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0002_alter_departamentos_options_fileupdate"),
    ]

    operations = [
        migrations.AddField(
            model_name="productos",
            name="imagen",
            field=models.ImageField(null=True, upload_to="productos_ventas/"),
        ),
    ]
