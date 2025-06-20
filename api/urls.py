from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DepartamentoApiView, ProductosApiView, VentaApiView, ProductXDeptoListView
from .views import FicherosSubidosApiView, SaldoEfectivoView, ContadorBilleteView
from .views import AlmacenApiView, ProductoApiView, PrecioProductoApiView, ContadorBilleteListView
from .views import CompraApiView, NominaDepartamentosApiView, NominaCargoApiView
from .views import ProduccionListView, SalidaListView, ProduccionProductoListView, CategoriaListView, DestinoListView

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

######## Saldos Cuentas y Contador de Billetes  #########
router.register(prefix="saldo_efectivo", viewset=SaldoEfectivoView, basename="saldoefectivo")
router.register(prefix="contador_billetes", viewset=ContadorBilleteView, basename="contadorbilletes")
router.register(prefix="contador_billetes_list", viewset=ContadorBilleteListView, basename="contadorbilleteslist")


######## Produccion #########
router.register(prefix="produccion_produccion", viewset=ProduccionListView, basename="produccion")
router.register(prefix="produccion_salida", viewset=SalidaListView, basename="salida")
router.register(prefix="produccion_producto", viewset=ProduccionProductoListView, basename="produccion_producto")
router.register(prefix="produccion_categoria", viewset=CategoriaListView, basename="categoria")
router.register(prefix="produccion_destino", viewset=DestinoListView, basename="destino")

# Están en ventas.urls
# urlpatterns = [
#     path('ventas_fechas/', VentasPorFechas.as_view(), name="ventas_fechas"),
#     path('suma_fechas/', SumaPorFechas.as_view(), name="suma_por_fechas")
# ]
