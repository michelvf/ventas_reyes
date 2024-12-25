from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, TransaccionCreateView
from .views import DashboardView, TransaccionListView, ExistenciaMensualView, VentaCreateView
from .views import VentaList, DetalleVentaList, ClienteList


urlpatterns = [
    path('', ProductoListView.as_view(), name='producto_list'),
    path('producto/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('transaccion/nueva/', TransaccionCreateView.as_view(), name='transaccion_create'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_puntoventa'),
    path('transacciones/', TransaccionListView.as_view(), name='transaccion_list'),
    path('existencia-mensual/', ExistenciaMensualView.as_view(), name='existencia_mensual'),
    path('venta_nueva/', VentaCreateView.as_view(), name='venta_create'),
    path('venta_list/', VentaList.as_view(), name='venta_list'),
    path('detalle_venta_list/', DetalleVentaList.as_view(), name='detalle_venta_list'),
    path('cliente_list/', ClienteList.as_view(), name='cliente_list'),
    
]
