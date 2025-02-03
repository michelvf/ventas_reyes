# tasks.py
from celery import shared_task
from .signals import actualizar_resumen_ventas
from ventas.models import Ventas

@shared_task
def actualizar_resumenes():
    for venta in Ventas.objects.all():
        actualizar_resumen_ventas(sender=Ventas, instance=venta)
