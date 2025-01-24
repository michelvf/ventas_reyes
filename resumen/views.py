from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum
import datetime
from ventas.models import Ventas

class ReporteVentasView(TemplateView):
    template_name = 'resumen/reporte_ventas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ahora = timezone.now()

        # Calcular ventas semanales
        inicio_semana = ahora - datetime.timedelta(days=ahora.weekday())
        context['ventas_semanales'] = Ventas.objects.filter(fecha__gte=inicio_semana).aggregate(total=Sum('calculo'))['total']

        # Calcular ventas mensuales
        inicio_mes = ahora.replace(day=1)
        context['ventas_mensuales'] = Ventas.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum('calculo'))['total']

        # Calcular ventas trimestrales
        inicio_trimestre = (ahora.month - 1) // 3 * 3 + 1
        inicio_trimestre = ahora.replace(month=inicio_trimestre, day=1)
        context['ventas_trimestrales'] = Ventas.objects.filter(fecha__gte=inicio_trimestre).aggregate(total=Sum('calculo'))['total']

        # Calcular ventas semestrales
        inicio_semestre = 1 if ahora.month <= 6 else 7
        inicio_semestre = ahora.replace(month=inicio_semestre, day=1)
        context['ventas_semestrales'] = Ventas.objects.filter(fecha__gte=inicio_semestre).aggregate(total=Sum('calculo'))['total']

        # Calcular ventas anuales
        inicio_año = ahora.replace(month=1, day=1)
        context['ventas_anuales'] = Ventas.objects.filter(fecha__gte=inicio_año).aggregate(total=Sum('calculo'))['total']

        return context
