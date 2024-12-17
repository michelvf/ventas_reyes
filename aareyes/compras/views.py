from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Sum, F
from django.urls import reverse_lazy
from datetime import timedelta
from .models import Almacen, Producto, Compra, PrecioProducto
from .forms import CompraForm, AlmacenForm, ProductoForm, PrecioProductoForm


class RegistrarAlmacenView(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/almacen/'
    # context_object_name = 'almacen'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Almacen"
        context["texto2"] = "Se agrega un nuevo almacén que contendrá varios productos y así ir organizando los productos."
        
        return context


class RegistrarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/productos/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Producto"
        context["texto2"] = "Escriba el nombre del producto y después escoja un Almacén, si el almacén no esta listado, debe agregarlo"
        
        return context


class RegistrarPrecioProductoView(CreateView):
    model = PrecioProducto
    form_class = PrecioProductoForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/resumen_semanal/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar un Producto y su precio"
        context["texto2"] = "Escoja el producto y después, escriba el precio"
        
        return context


class RegistrarCompraView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name =  'compras/registrar_compra.html'
    context_object_name = 'resumen'
    success_url = '/compras/resumen_semanal/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar una Compra"
        context["texto2"] = "Escoja un producto, después escriba la cantidad comprada, y después el precio"
        
        return context

########## Actualizar ##############
class ActualizarAlmacen(UpdateView):
    """
    Update the records
    """
    model = Almacen
    fields = ["nombre"]
    # template_name_suffix = "_update"
    template_name = 'compras/editar_compra.html'
    success_url = reverse_lazy('list_almacen')


class ActualizarProducto(UpdateView):
    """
    Update the records
    """
    model = Producto
    fields = ["nombre", "imagen", "almacen"]
    # template_name_suffix = "_update"
    template_name = 'compras/editar_compra.html'
    success_url = reverse_lazy('list_productos')


######## Borrar ################
class BorrarAlmacen(DeleteView):
    """
    Delete the records
    """
    model = Almacen
    # template_name_suffix = "_update"
    template_name = 'compras/borrar_compra.html'
    success_url = reverse_lazy('list_almacen')



class AlmacenListView(ListView):
    model = Almacen
    template_name = 'compras/almacen_list.html'


class ProductosListView(ListView):
    model = Producto
    template_name = 'compras/productos_list.html'


class PrecioProductoListView(ListView):
    model = PrecioProducto
    template_name = 'compras/precio_producto_list.html'


class CompraListView(ListView):
    model = Compra
    template_name = 'compra/compra_list.html'


class ResumeSemanalView(ListView):
    model = Compra
    template_name =  'compras/resumen_semanal.html'
    context_object_name = 'resumen'
    
    def get_queryset(self):
        hace_una_semana = timezone.now() - timedelta(days=7)
        return (Compra.objects.filter(fecha__gte=hace_una_semana)
            .values('producto__almacen__nombre', 'producto__nombre', 'fecha')
            .annotate(
                total_comprado=Sum('cantidad'),
                gasto_total=Sum(F('cantidad') * F('precio_compra'))
            )
            .order_by('producto__almacen__nombre'))
