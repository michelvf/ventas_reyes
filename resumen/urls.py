from django.urls import path
from .views import ReporteVentasView

urlpatterns = [
    path('reporte-ventas/', ReporteVentasView.as_view(), name='reporte_ventas'),
]