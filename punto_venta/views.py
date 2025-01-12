from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Producto, Envio, Venta, Almacen, Cliente, PuntoDeVenta
from .models import Proveedor, Categoria
from .forms import ProductoForm, EnvioForm, VentaForm, ClienteForm, ProveedorForm
from .forms import CategoriaForm, PuntoDeVentaForm, AlmacenForm
from django.views.generic import TemplateView
from django.utils import timezone


######### List ########
class ClienteListView(ListView):
    """
    Vista Listado de Clientes
    """
    model = Cliente
    template_name = 'punto_venta/cliente_list.html'
    context_object_name = 'clientes'


class ProductoListView(ListView):
    """
    Vista Listado de Producto
    """
    model = Producto
    template_name = 'punto_venta/producto_list.html'
    context_object_name = 'productos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Productores"
        
        return context


class EnvioListView(ListView):
    """
    Vista Listado de Envios
    """
    model = Envio
    template_name = 'punto_venta/envios_list.html'
    context_object_name = 'envios'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Envios"
        
        return context


class VentaListView(ListView):
    """
    Vista Listado de Venta
    """
    model = Venta
    template_name = 'punto_venta/venta_list.html'
    context_object_name = 'ventas'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Ventas"
        
        return context


class ProveedorListView(ListView):
    """
    Vista Listado de Envios
    """
    model = Proveedor
    template_name = 'punto_venta/proveedor_list.html'
    context_object_name = 'proveedores'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Proveedores"
        
        return context


class AlmacenListView(ListView):
    """
    Vista Listado de Almacen
    """
    model = Almacen
    template_name = 'punto_venta/almacen_list.html'
    context_object_name = 'almacenes'


class PuntoDeVentaListView(ListView):
    """
    Vista Listado de PuntoDeVentas
    """
    model = PuntoDeVenta
    template_name = 'punto_venta/puntodeventa_list.html'
    context_object_name = 'puntodeventas'


class CategoriaListView(ListView):
    """
    Vista Listado de Categorias
    """
    model = Categoria
    template_name = 'punto_venta/categoria_list.html'
    context_object_name = 'categorias'


class CierreCajaView(ListView):
    """
    Vista Listar CierreCaja
    """
    model = Venta
    template_name = 'punto_venta/cierre_caja.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        return Venta.objects.filter(punto_de_venta=self.request.user.puntodeventa, fecha__date=timezone.now().date())


############### Create View ###########
class ProductoCreateView(CreateView):
    """
    Vista Crear Producto
    """
    model = Producto
    form_class = ProductoForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('producto_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Productos"
        
        return context


class EnvioCreateView(CreateView):
    """
    Vista Crear Envio
    """
    model = Envio
    form_class = EnvioForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('envio_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Envíos"
        
        return context


class VentaCreateView(CreateView):
    """
    Vista Crear Ventas
    """
    model = Venta
    form_class = VentaForm
    template_name = 'punto_venta/venta_form.html'
    success_url = reverse_lazy('venta_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Ventas"
        
        return context
    


class ProveedorCreateView(CreateView):
    """
    Vista Crear Proveedor
    """
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('proveedor_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Proveedores"
        
        return context


class CategoriaCreateView(CreateView):
    """
    Vista Crear Categoria
    """
    model = Categoria
    form_class = CategoriaForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('categoria_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Categorías"
        
        return context


class PuntoDeVentaCreateView(CreateView):
    """
    Vista Crear Punto de Venta
    """
    model = PuntoDeVenta
    form_class = PuntoDeVentaForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('puntodeventa_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Punto de Ventas"
        
        return context


class ClienteCreateView(CreateView):
    """
    Vista Crear Cliente
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('cliente_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Clientes"
        
        return context


class AlmacenCreateView(CreateView):
    """
    Vista Crear Almacen
    """
    model = Almacen
    form_class = AlmacenForm
    template_name = 'punto_venta/producto_form.html'
    success_url = reverse_lazy('almacen_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["URL"] = "/api/nomina_departamentos/"
        context["Titulo"] = "Almacenes"
        
        return context

    
######### Query ##########
class InventarioRestanteView(TemplateView):
    template_name = 'inventory/inventario_restante.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto_id = self.request.GET.get('producto_id')
        almacen_id = self.request.GET.get('almacen_id')
        punto_de_venta_id = self.request.GET.get('punto_de_venta_id')
        fecha = self.request.GET.get('fecha')

        producto = Producto.objects.get(id=producto_id)
        almacen = Almacen.objects.get(id=almacen_id) if almacen_id else None
        punto_de_venta = PuntoDeVenta.objects.get(id=punto_de_venta_id) if punto_de_venta_id else None

        if almacen:
            context['inventario_restante'] = producto.inventario_en_almacen(almacen, fecha)
        elif punto_de_venta:
            context['inventario_restante'] = producto.inventario_en_punto_de_venta(punto_de_venta, fecha)

        context['producto'] = producto
        context['almacen'] = almacen
        context['punto_de_venta'] = punto_de_venta
        context['fecha'] = fecha

        return context
