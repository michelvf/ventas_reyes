# Generated by Django 5.1.4 on 2024-12-30 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0004_alter_productos_imagen"),
    ]

    operations = [
        migrations.AddField(
            model_name="departamentos",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
    ]
