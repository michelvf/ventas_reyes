from django.urls import path
from .views import ExcelUploadView, ShowVentas
from .views import ShowDepartamentos, ShowProductos, ShowEntreFechas
from api.views import VentasPorFechas
from django.views.generic import TemplateView



urlpatterns = [
    path('upload/', ExcelUploadView.as_view(), name='upload'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('datos/', ShowVentas.as_view(), name='showventas'),
    path('productos/', ShowProductos.as_view(), name='showProductos'),
    path('departamentos/', ShowDepartamentos.as_view(), name='showdepartamentos'),
    path('entrefechas/', ShowEntreFechas.as_view(), name='showentrefechas'),
    path('ventasfechas/', VentasPorFechas.as_view(), name='ventasporfechas'),
]

