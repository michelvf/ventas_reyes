from django.shortcuts import render
from .models import Trabajador, DepartamentoNom, Nomina, Cargo
from django.views.generic import ListView
from django.views import View


# Create your views here.
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
        return Cargo.objects.filter(activo= True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = ""
        
        return context
    

class TrabajdorList(ListView):
    """
    List of Departament
    """
    model = Trabajador
    template_name = 'nomina/trabadjores_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        # context["Titulo"] = " | Trabajadores"
        
        return context


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


