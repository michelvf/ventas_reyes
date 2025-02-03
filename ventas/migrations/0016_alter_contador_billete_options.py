from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ventas", "0015_alter_contador_billete_cien_pesos_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contador_billete",
            options={
                "ordering": ["-fecha"],
                "verbose_name": "contador_billete",
                "verbose_name_plural": "contador_billetes",
            },
        ),
    ]
