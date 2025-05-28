from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Producto, Produccion, Salida, Categoria
from .forms import ProduccionForm, SalidaForm, ProductoForm, CategoriaForm

# Vista para listar productos y su stock
class ProductoListView(ListView):
    """
    Vista ProductoList
    """
    model = Producto
    template_name = "produccion/productosLista.html"
    context_object_name = "productos"


class ProductoCreateView(CreateView):
    """
    Vista ProductoList, en app Produccion
    """
    model = Producto
    form_class = ProductoForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy('productos_list')


# Vista para registrar producción
class ProduccionCreateView(CreateView):
    """
    Vista ProductoCreate
    """
    model = Produccion
    form_class = ProduccionForm
    template_name = "produccion/produccionForm.html"
    success_url = reverse_lazy("productos_list")


# Vista para registrar salida de productos
class SalidaCreateView(CreateView):
    """
    Vista SalidaCreate
    """
    model = Salida
    form_class = SalidaForm
    template_name = "salidas/salidaForm.html"
    success_url = reverse_lazy("productos_list")


def clean_cantidad(self):
    cantidad = self.cleaned_data.get("cantidad")
    producto = self.cleaned_data.get("producto")
    if cantidad > producto.stock_actual:
        raise forms.ValidationError("No hay suficiente stock disponible")
    return cantidad