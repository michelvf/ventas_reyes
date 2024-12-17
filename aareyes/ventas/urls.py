from django.urls import path
from .views import ExcelUploadView, ShowVentas, SumarPorFechas, ProdxDepto
from .views import ShowDepartamentos, ShowProductos, ShowEntreFechas
from .views import LacteosVendidos, ProdMasVendido, ListadoFicherosSubidos
from api.views import VentasPorFechas, SumaPorFechasAPI, ProductXDeptoListView
from api.views import ProductMasVendidoAPI, LacteosAPI, FicherosSubidosApiView
from api.views import VentaSemanalAPI, LacteosSemanaAPI
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
    

    # Las API
    path('api_ventasfechas/', VentasPorFechas.as_view(), name='ventasporfechas'),
    path('api_suma_fechas/', SumaPorFechasAPI.as_view(), name="suma_por_fechas_api"),
    path('api_prod_x_depto/', ProductXDeptoListView.as_view(), name="prod_x_depto_api"),
    path('api_prod_mas_vendidos/', ProductMasVendidoAPI.as_view(), name="prod_mas_vendidos"),
    path('api_ventasemanal/', VentaSemanalAPI.as_view(), name="api_ventasemanal"),
    path('api_lacteos/', LacteosAPI.as_view(), name="api_lacteos"),
    path('api_lacteossemanal/', LacteosSemanaAPI.as_view(), name="api_lacteossemanal"),
    
]

