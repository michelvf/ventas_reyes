from django.urls import path
from .views import ExcelUploadView, ShowVentas, SumarPorFechas, ProdxDepto
from .views import ShowDepartamentos, ShowProductos, ShowEntreFechas
from .views import LacteosVendidos, ProdMasVendido, ListadoFicherosSubidos
from .views import  BackupRestoreSQLiteView, CalculadoraBilletes, DepartamentoUpdateView
from .views import VentasAnualesView, VentasMensualesView, VentasSemanalesView
from .views import ShowContadorBilletes, EditarCalculadoraBilletes, DondeSeVendeMas
from .views import DiaQueVendeMas, LacteosListView, LacteosCreate, LacteosUpdate
from .views import CalculoPorcientoPrecio
from api.views import VentasPorFechas, SumaPorFechasAPI, ProductXDeptoListView
from api.views import ProductMasVendidoAPI, LacteosAPI, FicherosSubidosApiView
from api.views import VentaSemanalAPI, LacteosSemanaAPI, DondeSeVendeMasAPI
from django.views.generic import TemplateView

urlpatterns = [
    path('upload/', ExcelUploadView.as_view(), name='upload'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    # path('datos/', ShowVentas.as_view(), name='showventas'),
    path('productos/', ShowProductos.as_view(), name='showProductos'),
    path('departamentos/', ShowDepartamentos.as_view(), name='showdepartamentos'),
    path('entrefechas/', ShowEntreFechas.as_view(), name='showentrefechas'),
    path('suma_fechas/', SumarPorFechas.as_view(), name="suma_por_fechas"),
    path('prod_x_dpto/', ProdxDepto.as_view(), name="prod_x_dpto"),
    path('prod_mas_vendido/', ProdMasVendido.as_view(), name="prod_mas_dpto"),
    path('lacteos/', LacteosVendidos.as_view(), name='lacteos'),
    path('ficherosSubidos/', ListadoFicherosSubidos.as_view(), name='ficherosSubidos'),
    path('backup_restore/', BackupRestoreSQLiteView.as_view(), name='backup_restore'),
    path('calculadora_billetes/', CalculadoraBilletes.as_view(), name='calculadora_billetes'),
    path('actualizar_departamentos/', DepartamentoUpdateView.as_view(), name='actualizar_departamentos'),
    path('mostrar_conteo_billetes/', ShowContadorBilletes.as_view(), name='mostrar_conteo_billetes'),
    path('editar_calculadora_billetes/<int:pk>/', EditarCalculadoraBilletes.as_view(), name='editar_calculadora_billetes'),
    path('reporte-mensual-departamento/', DondeSeVendeMas.as_view(), name='reporte_mensual_departamento'),
    path('reporte-venta-mensual/', DiaQueVendeMas.as_view(), name='reporte_venta_mensual'),
    path('porciento-precio/', CalculoPorcientoPrecio.as_view(), name='porciento_precio'),
    # path('estudio-inventario/', EstudioInventario.as_view(), name='estudio_inventario'),
    
    path('listado_lacteos/', LacteosListView.as_view(), name='listado_lacteos'),
    path('crear_lacteos/', LacteosCreate.as_view(), name='crear_lacteos'),
    path('editar_lacteos/<int:pk>', LacteosUpdate.as_view(), name='editar_lacteos'),
    
    path("<int:year>/", VentasAnualesView.as_view(), name="ventas_anuales"),
    path("<int:year>/<int:month>/", VentasMensualesView.as_view(month_format="%m"), name="ventas_mensuales"),
    path("<int:year>/week/<int:week>/", VentasSemanalesView.as_view(), name="ventas_semanales"),

    # Las API
    path('api_ventasfechas/', VentasPorFechas.as_view(), name='ventasporfechas'),
    path('api_suma_fechas/', SumaPorFechasAPI.as_view(), name="suma_por_fechas_api"),
    path('api_prod_x_depto/', ProductXDeptoListView.as_view(), name="prod_x_depto_api"),
    path('api_prod_mas_vendidos/', ProductMasVendidoAPI.as_view(), name="prod_mas_vendidos"),
    path('api_ventasemanal/', VentaSemanalAPI.as_view(), name="api_ventasemanal"),
    path('api_lacteos/', LacteosAPI.as_view(), name="api_lacteos"),
    path('api_lacteossemanal/', LacteosSemanaAPI.as_view(), name="api_lacteossemanal"),
    path('api_dondesevendemas/', DondeSeVendeMasAPI.as_view(), name="api_dondesevendemas"),
    
    
]

