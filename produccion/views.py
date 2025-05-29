from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Producto, Produccion, Salida, Categoria
from .forms import ProduccionForm, SalidaForm, ProductoForm, CategoriaForm

# Categoría
class CategoriaListView(ListView):
    """
    Vista CategoriaList
    """
    model = Categoria
    template_name = "produccion/categoriasLista.html"
    context_object_name = "categorias"


class CategoriaCreateView(CreateView):
    """
    Vista CategoriaCreate
    """
    model = Categoria
    form_class = CategoriaForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("categorias_list")


class CategoriaUpdateView(UpdateView):
    """
    Vista CategoriaUpdate
    """
    model = Categoria
    form_class = CategoriaForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("categorias_list")


class CategoriaDeleteView(DeleteView):
    """
    Vista CategoriaDelete
    """
    model = Categoria
    template_name = "produccion/Borrar.html"
    success_url = reverse_lazy("categorias_list")



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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar un Producto"
        context["texto1"] = "Agregar un Producto"
        context["texto2"] = "Se agrega un nuevo producto."
        
        return context

class ProductoUpdateView(UpdateView):
    """
    Vista ProductoUpdate
    """
    model = Producto
    form_class = ProductoForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("productos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar un Producto"
        context["texto2"] = "Se actualiza un producto."
        
        return context


class ProductoDeleteView(DeleteView):
    """
    Vista ProductoDelete
    """
    model = Producto
    template_name = "produccion/productosDelete.html"
    success_url = reverse_lazy("productos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar un Producto"
        context["texto1"] = "Eliminar un Producto"
        context["texto2"] = "Se elimina un producto."
        
        return context


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