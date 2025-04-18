# Generated by Django 5.1.3 on 2024-12-18 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compras", "0007_alter_producto_imagen"),
    ]

    operations = [
        migrations.CreateModel(
            name="UnidadMedida",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("sigla", models.CharField(max_length=100)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "unidad_medida",
                "verbose_name_plural": "unidades_medidas",
                "ordering": ["nombre"],
                "indexes": [
                    models.Index(fields=["id"], name="compras_uni_id_2b4a58_idx"),
                    models.Index(
                        fields=["nombre"], name="compras_uni_nombre_c425ec_idx"
                    ),
                ],
            },
        ),
    ]
