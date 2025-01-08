from django.urls import path
from .views import ProductoListView, ClienteListView, AlmacenListView, CategoriaListView
from .views import ProveedorListView, VentaListView, CierreCajaView, PuntoDeVentaListView
from .views import EnvioListView
from .views import ProductoCreateView, VentaCreateView, EnvioCreateView
from .views import ProveedorCreateView, CategoriaCreateView, PuntoDeVentaCreateView
from .views import InventarioRestanteView, ClienteCreateView, AlmacenCreateView


urlpatterns = [
    ## List
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('cliente-list/', ClienteListView.as_view(), name='cliente_list'),
    path('proveedor-list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('categoria-list/', CategoriaListView.as_view(), name='categoria_list'),
    path('puntodeventa-list/', PuntoDeVentaListView.as_view(), name='puntodeventa_list'),
    path('venta-list/', VentaListView.as_view(), name='venta_list'),
    path('envio-list/', EnvioListView.as_view(), name='envio_list'),
    
    path('almacen-list/', AlmacenListView.as_view(), name='almacen_list'),
    
    ## Create
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto_create'),
    path('envios/nuevo/', EnvioCreateView.as_view(), name='envio_create'),
    path('ventas/nuevo/', VentaCreateView.as_view(), name='venta_create'),
    path('proveedor/nuevo/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('categoria/nuevo/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('puntodeventa/nuevo/', PuntoDeVentaCreateView.as_view(), name='puntodeventa_create'),
    path('cliente/nuevo', ClienteCreateView.as_view(), name='cliente_create'),
    path('almacen/nuevo', AlmacenCreateView.as_view(), name='almacen_create'),
    path('cierre-caja/', CierreCajaView.as_view(), name='cierre_caja'),
    
    ## Update
    ## Query
    path('inventario-restante/', InventarioRestanteView.as_view(), name='inventario_restante'),
]
