from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DepartamentoApiView, ProductosApiView, VentaApiView, ProductXDeptoListView
from .views import FicherosSubidosApiView
from .views import AlmacenApiView, ProductoApiView, PrecioProductoApiView
from .views import CompraApiView, NominaDepartamentosApiView, NominaCargoApiView

router = DefaultRouter()

####### Gestion  ######
router.register(prefix="departamentos", basename="departamentos", viewset=DepartamentoApiView)
router.register(prefix="productos", basename="productos", viewset=ProductosApiView)
router.register(prefix="ventas", basename="ventas", viewset=VentaApiView)
router.register(prefix="ficherosubidos", basename="ficherossubidos", viewset=FicherosSubidosApiView)

######### Compra #########
router.register(prefix="almacen", viewset=AlmacenApiView, basename="almacen")
router.register(prefix="producto", viewset=ProductoApiView, basename="producto")
router.register(prefix="precioproducto", viewset=PrecioProductoApiView, basename="precioproducto")
router.register(prefix="compra", viewset=CompraApiView, basename="compra")

######### Nomina ##########
router.register(prefix="nomina_departamentos", viewset=NominaDepartamentosApiView, basename="nomina_departamentos")
router.register(prefix="nomina_cargos", viewset=NominaCargoApiView, basename="nomina_cargos")


# Están en ventas.urls
# urlpatterns = [
#     path('ventas_fechas/', VentasPorFechas.as_view(), name="ventas_fechas"),
#     path('suma_fechas/', SumaPorFechas.as_view(), name="suma_por_fechas")
# ]
