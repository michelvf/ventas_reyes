from django.urls import path
from .views import DepartamentoList, CargoList, TrabajdorList, NominaList
from .views import RegistrarCargosView, RegistrarTrabajadorView, RegistrarNominaView
from .views import ActualizarCargo, ActualizarNomina, ActualizarTrabajador

urlpatterns = [
    ### Listdos
    path('cargos/', CargoList.as_view(), name='nomina_cargos'),
    path('departamentos/', DepartamentoList.as_view(), name='nomina_departamentos'),
    path('trabajadores/', TrabajdorList.as_view(), name='nomina_trabajadores'),
    path('nomina/', NominaList.as_view(), name='nomina_list'),
    
    ### Registrar
    path('registrar_cargo/', RegistrarCargosView.as_view(), name='registrar_cargo'),
    path('registrar_trabajador/', RegistrarTrabajadorView.as_view(), name='registrar_trabajador'),
    path('registrar_nomina/', RegistrarNominaView.as_view(), name='registrar_nomina'),

  
    ### Actualizar
    path('actualizar_cargo/<int:pk>/', ActualizarCargo.as_view(), name='actualizar_cargo'),
    path('actualizar_nomina/<int:pk>/', ActualizarNomina.as_view(), name='actualizar_nomina'),
    path('actualizar_trabajador/<int:pk>/', ActualizarTrabajador.as_view(), name='actualizar_trabajador'),
    

 ]
