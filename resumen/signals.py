# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ResumenVentas
from ventas.models import Ventas
from django.db.models import Sum

@receiver(post_save, sender=Ventas)
def actualizar_resumen_ventas(sender, instance, **kwargs):
    """
    Signal para guardar la estadística en el tiempo
    """
    ahora = timezone.now()
    inicio_semana = ahora - timezone.timedelta(days=ahora.weekday())
    inicio_mes = ahora.replace(day=1)
    inicio_trimestre = (ahora.month - 1) // 3 * 3 + 1
    inicio_trimestre = ahora.replace(month=inicio_trimestre, day=1)
    inicio_semestre = 1 if ahora.month <= 6 else 7
    inicio_semestre = ahora.replace(month=inicio_semestre, day=1)
    inicio_año = ahora.replace(month=1, day=1)
    
    totales = {
        'semanal': Ventas.objects.filter(fecha__gte=inicio_semana).aggregate(total=Sum('calculo'))['total'],
        'mensual': Ventas.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum('calculo'))['total'],
        'trimestral': Ventas.objects.filter(fecha__gte=inicio_trimestre).aggregate(total=Sum('calculo'))['total'],
        'semestral': Ventas.objects.filter(fecha__gte=inicio_semestre).aggregate(total=Sum('calculo'))['total'],
        'anual': Ventas.objects.filter(fecha__gte=inicio_año).aggregate(total=Sum('calculo'))['total'],
    }

    for periodo, total in totales.items():
        # print(f"Período: {periodo}, Total: {total}")
        resumen, creado = ResumenVentas.objects.get_or_create(periodo=periodo, total_vendido=total or 0)
        # print('El dúo, resumen: {resumen}, creado: {creado}')
        # resumen.total_vendido = total or 0
        # resumen.save()
