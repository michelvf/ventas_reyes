from django.urls import path
from .views import ReporteVentasView
from api.views import DiaQueVendeMas, AnnosDeVenta

urlpatterns = [
    path('reporte-ventas/', ReporteVentasView.as_view(), name='reporte_ventas'),
    
    
    #### API ###
    path('dia_mas_venta/', DiaQueVendeMas.as_view(), name='dia_mas_venta'),
    path('anno_venta/', AnnosDeVenta.as_view(), name='anno_venta'),
    
]