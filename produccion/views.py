from ast import Del, List
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Producto, Produccion, Salida, Categoria, Destino
from .forms import ProduccionForm, SalidaForm, ProductoForm, CategoriaForm, DestinoForm

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
    Vista ProductoUpdate, en app Produccion
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
    Vista ProductoDelete, en app Produccion
    """
    model = Producto
    template_name = "produccion/Borrar.html"
    success_url = reverse_lazy("productos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar un Producto"
        context["texto1"] = "Eliminar un Producto"
        context["texto2"] = "Se elimina un producto."
        
        return context


# Vista para registrar producción
class ProduccionListView(ListView):
    """
    Vista ProduccionList, en app Produccion
    """
    model = Produccion
    template_name = "produccion/produccionLista.html"
    context_object_name = "producciones"


class ProduccionCreateView(CreateView):
    """
    Vista ProduccionCreate, en app Produccion
    """
    model = Produccion
    form_class = ProduccionForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("produccion_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar una Producción"
        context["texto1"] = "Agregar una Producción"
        context["texto2"] = "Se agrega una producción."
        
        return context


class ProduccionUpdateView(UpdateView):
    """
    Vista ProduccionUpdate, en app Produccion
    """
    model = Produccion
    form_class = ProduccionForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("produccion_list")
    
    def form_valid(self, form):
        """
        Override form_valid to adjust stock based on quantity changes
        """
        # Get the current production record
        produccion = self.get_object()
        producto = produccion.producto
        cantidad_anterior = produccion.cantidad
        
        # Get the new quantity from the form
        cantidad_nueva = form.cleaned_data['cantidad']
        
        # Calculate the difference
        diferencia = cantidad_nueva - cantidad_anterior
        
        # Update stock based on the difference
        producto.stock_actual += diferencia
        producto.save()
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar la Producción"
        context["texto2"] = "Se actualiza una producción."
        
        return context


class ProduccionDeleteView(DeleteView):
    """
    Vista ProduccionDelete, en app Produccion
    """
    model = Produccion
    template_name = "produccion/Borrar.html"
    success_url = reverse_lazy("produccion_list")
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to update stock before deletion
        """
        self.object = self.get_object()
        # Get the product and its quantity
        producto = self.object.producto
        cantidad = self.object.cantidad
        
        # Update stock
        producto.stock_actual -= cantidad
        producto.save()
        
        # Proceed with deletion
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar una Producción"
        context["texto1"] = "Eliminar una Producción"
        context["texto2"] = "Se elimina una producción."
        
        return context


# Vista para registrar salida de productos
class SalidaListView(ListView):
    """
    Vista SalidaList, en app Produccion
    """
    model = Salida
    template_name = "produccion/salidaLista.html"
    context_object_name = "salidas"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Listado de Salidas"
        context["texto1"] = "Listado de Salidas"
        context["texto2"] = "Se listan las salidas."
        
        return context


class SalidaCreateView(CreateView):
    """
    Vista SalidaCreate, en app Produccion
    """
    model = Salida
    form_class = SalidaForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("productos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar una Salida"
        context["texto1"] = "Agregar una Salida"
        context["texto2"] = "Se agrega una salida."
        
        return context


class SalidaUpdateView(UpdateView):
    """
    Vista SalidaUpdate, en app Produccion
    """
    model = Salida
    form_class = SalidaForm
    template_name = "produccion/salidaForm.html"
    success_url = reverse_lazy("productos_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar una Salida"
        context["texto2"] = "Se actualiza una salida."
        
        return context

class SalidaDeleteView(DeleteView):
    """
    Vista SalidaDelete, en app Produccion
    """
    model = Salida
    template_name = "produccion/Borrar.html"   
    success_url = reverse_lazy("productos_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar una Salida"
        context["texto1"] = "Eliminar una Salida"
        context["texto2"] = "Se elimina una salida."
        
        return context


### Destino
class DestinoListView(ListView):
    """
    Vista DestinoList, en app Produccion
    """
    model = Destino
    template_name = "produccion/destinoLista.html"
    context_object_name = "destinos"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Listado de Destinos"
        context["texto1"] = "Listado de Destinos"
        context["texto2"] = "Se listan los destinos."
        
        return context


class DestinoCreateView(CreateView):
    """
    Vista DestinoCreate, en app Produccion
    """
    model = Destino
    form_class = DestinoForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("destino_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar un Destino"
        context["texto1"] = "Agregar un Destino"
        context["texto2"] = "Se agrega un nuevo destino."
        
        return context


class DestinoUpdateView(UpdateView):
    """
    Vista DestinoUpdate, en app Produccion
    """
    model = Destino
    form_class = DestinoForm
    template_name = "produccion/productosForm.html"
    success_url = reverse_lazy("destino_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Actualizar un Destino"
        context["texto2"] = "Se actualiza un destino."
        
        return context


class DestinoDeleteView(DeleteView):
    """
    Vista DestinoDelete, en app Produccion
    """
    model = Destino
    template_name = "produccion/Borrar.html"
    success_url = reverse_lazy("destino_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Eliminar un Destino"
        context["texto1"] = "Eliminar un Destino"
        context["texto2"] = "Se elimina un destino."
        
        return context


# def clean_cantidad(self):
#     cantidad = self.cleaned_data.get("cantidad")
#     producto = self.cleaned_data.get("producto")
#     if cantidad > producto.stock_actual:
#         raise forms.ValidationError("No hay suficiente stock disponible")
#     return cantidad