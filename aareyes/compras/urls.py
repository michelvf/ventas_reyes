from django.urls import path

from .views import RegistrarPrecioProductoView, RegistrarCompraView, RegistrarProductoView, RegistrarAlmacenView
from .views import ProductosListView, PrecioProductoListView, CompraListView, AlmacenListView
from .views import ActualizarAlmacen, ActualizarProducto, ActualizarPrecioProducto, ActualizarCompra
from .views import BorrarAlmacen, BorrarCompra
from .views import ResumeSemanalView, ResumenProductoSemanalView
from api.views import UltimoPrecio


urlpatterns = [
    # Listado
    path('almacen/', AlmacenListView.as_view(), name='list_almacen'),
    path('productos/', ProductosListView.as_view(), name='list_productos'),
    path('precio_productos/', PrecioProductoListView.as_view(), name='list_precio_productos'),
    path('compra/', CompraListView.as_view(), name='list_compra'),
    # Registrar
    path('registrar_almacen/', RegistrarAlmacenView.as_view(), name='registrar_almacen'),
    path('registrar_producto/', RegistrarProductoView.as_view(), name='registrar_producto'),
    path('registrar_precio_producto/', RegistrarPrecioProductoView.as_view(), name='registrar_precio_producto'),
    path('registrar_compra/', RegistrarCompraView.as_view(), name='registrar_compra'),
    # Editar
    path('editar_almacen/<int:pk>/', ActualizarAlmacen.as_view(), name='editar_almacen'),
    path('editar_producto/<int:pk>/', ActualizarProducto.as_view(), name='editar_producto'),
    path('editar_precioproducto/<int:pk>/', ActualizarPrecioProducto.as_view(), name='editar_precioproducto'),
    path('editar_compra/<int:pk>/', ActualizarCompra.as_view(), name='editar_compra'),
    # Borrar
    path('borrar_almacen/<int:pk>/', BorrarAlmacen.as_view(), name='borrar_almacen'),
    path('borrar_compra/<int:pk>/', BorrarCompra.as_view(), name='borrar_compra'),
    # Consultas
    path('resumen_semanal/', ResumeSemanalView.as_view(), name='resumen_semanal' ),
    path('resumen_productosemanal/', ResumenProductoSemanalView.as_view(), name='resumen_productosemanal' ),
    # API
    path('api_ultimoprecio/', UltimoPrecio.as_view(), name='ultimoprecio'),

]
