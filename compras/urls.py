from django.urls import path

from .views import RegistrarPrecioProductoView, RegistrarCompraView, RegistrarProductoView, RegistrarAlmacenView
from .views import AlmacenListView, PrecioProductoListView, CompraListView # ,ProductosListView
from .views import ActualizarAlmacen, ActualizarProducto, ActualizarPrecioProducto, ActualizarCompra
from .views import BorrarAlmacen, BorrarCompra
from .views import UnidadMedidaListView, UnidadMedidaCreateView, UnidadMedidaDetailView, UnidadMedidaUpdateView, UnidadMedidaDeleteView
from .views import ResumeSemanalView, ResumenProductoSemanalView, ResumenSemanalLecheView
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDetailView, ClienteDeleteView
from .views import ProductoCreateView, ProductoDeleteView, ProductoDetailView, ProductoListView, ProductosListView, ProductoUpdateView, get_producto_info
from .views import FacturaListView, FacturaDetailView, crear_factura, editar_factura, eliminar_factura, cambiar_estado_factura
from .views import VerFactura, PruebaBT, APIProductos, APIClientes, LeerExcel
from .excel_processor import ExcelProcessor
from api.views import UltimoPrecio, CompraLecheSemana
from . import views


urlpatterns = [
    # Listado
    path('almacen/', AlmacenListView.as_view(), name='list_almacen'),
   #  path('productos/', ProductosListView.as_view(), name='list_productos'),
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
    path('resumen_productolechesemanal/', ResumenSemanalLecheView.as_view(), name='resumen_productolechesemanal' ),
    # API
    path('api_ultimoprecio/', UltimoPrecio.as_view(), name='ultimoprecio'),
    path('api_compralechesemana/', CompraLecheSemana.as_view(), name='api_compralechesemana'),
    path('excel_procces/', ExcelProcessor, name='excel_procces'),
    path('excel_upload/', LeerExcel.as_view(), name='excel_leer'),

    # Unidad de Medida
    path('unidadmedida/', UnidadMedidaListView.as_view(), name='unidadmedida_list'),
    path('unidadmedida/<int:pk>/', UnidadMedidaDetailView.as_view(), name='unidadmedida_detail'),
    path('unidadmedida/nuevo/', UnidadMedidaCreateView.as_view(), name='unidadmedida_create'),
    path('unidadmedida/<int:pk>/editar/', UnidadMedidaUpdateView.as_view(), name='unidadmedida_update'),
    path('unidadmedida/<int:pk>/eliminar/', UnidadMedidaDeleteView.as_view(), name='unidadmedida_delete'),
    
    # Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # Productos
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),
    path('productos/info/', get_producto_info, name='producto_info'),
    
    # Facturas
    path('facturas/', FacturaListView.as_view(), name='factura_list'),
    path('facturas/<int:pk>/', FacturaDetailView.as_view(), name='factura_detail'),
    path('facturas/nueva/', crear_factura, name='factura_create'),
    path('facturas/<int:pk>/editar/', editar_factura, name='factura_update'),
    path('facturas/<int:pk>/eliminar/', eliminar_factura, name='factura_delete'),
    path('facturas/<int:pk>/estado/<str:estado>/', cambiar_estado_factura, name='factura_cambiar_estado'),
    
    # Ver Factura
    path('facturas/<int:pk>/ver/', VerFactura.as_view(), name='ver_factura'),
    path('facturas/<int:pk>/pdf/', views.factura_pdf, name='factura_pdf'),
    
    # API para actualización en tiempo real
    path('api/facturas/', views.get_facturas_json, name='api_facturas'),
    path('api/productos/', APIProductos.as_view(), name='api_productos'),
    path('api/clientes/', APIClientes.as_view(), name='api_clientes'),
    path('api/clientes/<int:cliente_id>/facturas/', views.get_facturas_cliente_json, name='api_facturas_cliente'),
    path('api/productos_facturas/', APIProductos.as_view(), name='api_productos_facturas'),

    # Pruebas
    path('pruebaBT/', PruebaBT.as_view(), name="pruebaBT"),
]
