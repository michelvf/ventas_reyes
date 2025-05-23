# Generated by Django 5.1.3 on 2024-12-02 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Departamentos",
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
                ("departamento", models.CharField(max_length=200)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "departmento",
                "verbose_name_plural": "departmentos",
                "ordering": ["departamento"],
                "indexes": [
                    models.Index(fields=["id"], name="ventas_depa_id_46f0dc_idx"),
                    models.Index(
                        fields=["departamento"], name="ventas_depa_departa_cb02f5_idx"
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Productos",
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
                ("codigo", models.IntegerField()),
                ("producto", models.CharField(max_length=200)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                (
                    "id_departamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="productos",
                        to="ventas.departamentos",
                    ),
                ),
            ],
            options={
                "verbose_name": "producto",
                "verbose_name_plural": "productos",
                "ordering": ["producto"],
            },
        ),
        migrations.CreateModel(
            name="Ventas",
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
                ("cantidad", models.FloatField()),
                ("venta", models.FloatField()),
                ("costo", models.FloatField()),
                ("calculo", models.FloatField()),
                ("fecha", models.DateTimeField()),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                (
                    "id_producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="productos",
                        to="ventas.productos",
                    ),
                ),
            ],
            options={
                "verbose_name": "venta",
                "verbose_name_plural": "ventas",
                "ordering": ["fecha"],
            },
        ),
        migrations.AddIndex(
            model_name="productos",
            index=models.Index(fields=["id"], name="ventas_prod_id_f6485c_idx"),
        ),
        migrations.AddIndex(
            model_name="productos",
            index=models.Index(fields=["codigo"], name="ventas_prod_codigo_8f6a90_idx"),
        ),
        migrations.AddIndex(
            model_name="productos",
            index=models.Index(
                fields=["producto"], name="ventas_prod_product_98c071_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="ventas",
            index=models.Index(fields=["id"], name="ventas_vent_id_6918a6_idx"),
        ),
        migrations.AddIndex(
            model_name="ventas",
            index=models.Index(fields=["fecha"], name="ventas_vent_fecha_ef75da_idx"),
        ),
        migrations.AddIndex(
            model_name="ventas",
            index=models.Index(
                fields=["id_producto"], name="ventas_vent_id_prod_9ca7d9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="ventas",
            index=models.Index(
                fields=["calculo"], name="ventas_vent_calculo_d50391_idx"
            ),
        ),
    ]
