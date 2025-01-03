from django.shortcuts import render
from .models import Trabajador, DepartamentoNom, Nomina, Cargo
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from .forms import CargoForm, TrabajadorForm, NominaForm
from django.urls import reverse_lazy, reverse
from django.utils import timezone


# Create your views here.

# ########## Listado #########
class DepartamentoList(ListView):
    """
    List of Departament
    """
    model = DepartamentoNom
    template_name = 'ventas/departamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["URL"] = "/api/nomina_departamentos/"
        
        return context


class CargoList(ListView):
    """
    List of Departament
    """
    model = Cargo
    template_name = 'nomina/cargos_list.html'
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Cargo.objects.filter(activo=True)
    
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = ""
        
        # return context


class TrabajdorList(ListView):
    """
    List of Departament
    """
    model = Trabajador
    template_name = 'nomina/trabajadores_list.html'
    
    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Trabajadores"
        
        # return context


class NominaList(ListView):
    """
    List of Departament
    """
    model = Nomina
    template_name = 'nomina/nomina_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Nómina"
        
        return context


# ########### Agregar #############
class RegistrarCargosView(CreateView):
    """
    Register warehouses
    """
    model = Cargo
    form_class = CargoForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/cargos/'
    # context_object_name = 'almacen'


    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_cargo')
        else:
            return reverse('nomina_cargos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Cargo"
        context["texto2"] = "Se agrega un nuevo cargo."
        
        return context


class RegistrarTrabajadorView(CreateView):
    """
    Register Worked
    """
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/trabajadores/'

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_trabajador')
        else:
            return reverse('nomina_trabajadores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Trabajador"
        context["texto2"] = "Se agrega un nuevo trabajador."

        return context


class RegistrarNominaView(CreateView):
    """
    Register Payroll
    """
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina/registrar_cargo.html'
    success_url = '/nomina/nomina/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un trabajador a la Nómina"
        context["texto2"] = "Se agrega un nuevo trabajador con el salario que va a cobrar, en la nómina."

        return context

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_nomina')
        else:
            return reverse('nomina_list')


# ########### Actializar ##########
class ActualizarCargo(UpdateView):
    """
    Update the records
    """
    model = Cargo
    # fields = ["cargo", "comentario", "activo"]
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_cargos')
    form_class = CargoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar el Cargo"
        context["texto2"] = "Se actualiza la información del Cargo."

        return context


class ActualizarNomina(UpdateView):
    """
    Update the records
    """
    model = Nomina
    # fields = ['trabajador', 'salario', 'fecha', 'activo']
    form_class = NominaForm
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar la Nómina"
        context["texto2"] = "Se actualiza la información de la Nómina."
        
        return context
    

class ActualizarTrabajador(UpdateView):
    """
    Update the records
    """
    model = Trabajador
    # fields = ['nombre', 'departamento', 'cargo', 'fecha', 'activo']
    form_class = TrabajadorForm
    # template_name_suffix = "_update"
    template_name = 'nomina/editar_nomina.html'
    success_url = reverse_lazy('nomina_trabajadores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar el Trabajador"
        context["texto2"] = "Se actualiza la información del Trabajador."
        
        return context