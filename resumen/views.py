from django.shortcuts import render
from django.views.generic import TemplateView, View
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


class Estadistica(View):
    """
    Estadística de las Ventas en el tiempo
    semanal, mensual, trimestral, semestral, anual
    """
    
    ventas = Ventas.objects.all()
    
    # Recorrer validadndo que la fecha = a la 1ra semana e ir cambiando
    # mientras van pasando las fechas
    #     ir sumando mienstras se va a recorriendo y hacer 0 el sunando
    #     cuando cambie de semana
    semana1 = 0
    mes1 = 0
    trimestre1 = 0
    anno1 = 0
    suma_semana = 0
    suma_mes = 0
    suma_trimestre = 0
    suma_anno = 0
    for venta in ventas:
        fecha = venta.fecha
        # days = fecha.weekday()
        semana = fecha.strftime('%V')
        mes = fecha.strftime('%m')
        anno = fecha.strftime('%Y')
        suma_semana += venta.calculo
        suma_mes += venta.calculo
        suma_trimestre += venta.calculo
        suma_anno += venta.calculo
        if semana != semana1:
            print(f"semana: {semana}-{anno}, sumatoria: {suma_semana} -- {fecha.strftime('%d/%m/%Y')}")
            semana1 = semana
            suma_semana = 0
        if mes1 != mes:
            print(f"mes: {mes}-{anno}, sumatoria: {suma_mes} -- {fecha.strftime('%d/%m/%Y')}")
            mes1 = mes
            suma_mes = 0