# Generated by Django 5.1.5 on 2025-03-27 09:52
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0017_lacteos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lacteos",
            options={"ordering": ["nombre"], "verbose_name_plural": "Lactetos"},
        ),
        migrations.AlterField(
            model_name="lacteos",
            name="nombre",
            field=models.CharField(max_length=50),
        ),
    ]
