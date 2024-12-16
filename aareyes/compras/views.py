from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta
from .models import Almacen, Producto, Compra, PrecioProducto
from .forms import CompraForm, AlmacenForm, ProductoForm, PrecioProductoForm


class RegistrarAlmacenView(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/resumen_semanal/'
    # context_object_name = 'almacen'


class RegistrarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/resumen_semanal/'


class RegistrarPrecioProductoView(CreateView):
    model = PrecioProducto
    form_class = PrecioProductoForm
    template_name = 'compras/registrar_compra.html'
    success_url = '/compras/resumen_semanal/'


class RegistrarCompraView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name =  'compras/registrar_compra.html'
    context_object_name = 'resumen'
    success_url = '/compras/resumen_semanal/'


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
