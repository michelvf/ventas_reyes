from django.apps import AppConfig


class ResumenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resumen"

    def ready(self):
        import resumen.signals