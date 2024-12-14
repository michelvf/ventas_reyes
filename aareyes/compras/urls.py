from django.urls import path

from .views import RegistrarCompraView, ResumeSemanalView, RegistrarAlmacenView
from .views import RegistrarProductoView, RegistrarPrecioProductoView

urlpatterns = [
    path('registrar_almacen/', RegistrarAlmacenView.as_view(), name='registrar_almacen'),
    path('registrar_producto/', RegistrarProductoView.as_view(), name='registrar_producto'),
    path('registrar_precio_producto/', RegistrarPrecioProductoView.as_view(), name='registrar_precio_producto'),
    path('registrar_compra/', RegistrarCompraView.as_view(), name='registrar_compra'),
    path('resumen_semanal/', ResumeSemanalView.as_view(), name='resumen_semanal' ),
]
