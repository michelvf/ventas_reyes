from django.urls import path
from .views import DepartamentoList, CargoList, TrabajdorList, NominaList

urlpatterns = [
    path('cargos/', CargoList.as_view(), name='nomina_cargos'),
    path('departamentos/', DepartamentoList.as_view(), name='nomina_departamentos'),
    path('trabajadores/', TrabajdorList.as_view(), name='nomina_trabajadores'),
    path('nomina/', NominaList.as_view(), name='nomina_list'),
 ]
