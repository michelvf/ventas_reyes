from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views import View
from django.utils import timezone
from django.db.models import Sum, F
from django.urls import reverse_lazy, reverse
from datetime import timedelta
from .models import Almacen, Producto, Compra, PrecioProducto, UnidadMedida
from .forms import CompraForm, AlmacenForm, ProductoForm, PrecioProductoForm
from .forms import ResumenSemanal
from rest_framework import authentication
from operator import itemgetter, attrgetter

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .models import Cliente, Producto, Factura, DetalleFactura
from .forms import ClienteForm, ProductoForm, FacturaForm, DetalleFacturaFormSet

import numpy as np


class RegistrarAlmacenView(CreateView):
    """
    Register warehouses
    """
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
    """
    Register Product
    """
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
    """
    Register Price and Product
    """
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
    """
    Register Purchases
    """
    model = Compra
    form_class = CompraForm
    template_name =  'compras/registrar_compra.html'
    context_object_name = 'resumen'
    # success_url = '/compras/compra/'

    def get_success_url(self):
        if 'guardar_y_seguir' in self.request.POST:
            return reverse('registrar_compra')
        else:
            return reverse('list_compra')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texto1"] = "Agregar una Compra"
        context["texto2"] = "Escoja un producto, después escriba la cantidad comprada, y después el precio"
        # context["compras"] = "onChange='select(this.value)'"
        
        return context


##########  Actualizar  ##############
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
    fields = ["nombre", "medida", "imagen", "almacen"]
    # template_name_suffix = "_update"
    template_name = 'compras/editar_compra.html'
    success_url = reverse_lazy('list_productos')


class ActualizarCompra(UpdateView):
    """
    Update the records
    """
    model = Compra
    #fields = ["producto", "cantidad", "precio_compra", "fecha"]
    # template_name_suffix = "_update"
    template_name = 'compras/editar_compra.html'
    success_url = reverse_lazy('list_compra')
    form_class = CompraForm


class ActualizarPrecioProducto(UpdateView):
    """
    Update the records
    """
    model = PrecioProducto
    fields = ["producto", "precio", "fecha"]
    # template_name_suffix = "_update"
    template_name = 'compras/editar_compra.html'
    success_url = reverse_lazy('list_precio_productos')


########  Borrar  ################
class BorrarAlmacen(DeleteView):
    """
    Delete the records
    """
    model = Almacen
    # template_name_suffix = "_update"
    template_name = 'compras/borrar_compra.html'
    success_url = reverse_lazy('list_almacen')


class BorrarCompra(DeleteView):
    """
    Delete the records
    """
    model = Compra
    # template_name_suffix = "_update"
    template_name = 'compras/borrar_compra.html'
    success_url = reverse_lazy('list_compra')


######  Listar  ########
class AlmacenListView(ListView):
    """
    List Store
    """
    model = Almacen
    template_name = 'compras/almacen_list.html'


class ProductosListView(ListView):
    """
    List Product
    """
    model = Producto
    template_name = 'compras/productos_list.html'


class PrecioProductoListView(ListView):
    """
    List Price of Product
    """
    model = PrecioProducto
    template_name = 'compras/precio_producto_list.html'


class CompraListView(ListView):
    """
    Shopping List
    """
    model = Compra
    template_name = 'compra/compra_list.html'


########## Resumenes ########
class ResumeSemanalView(ListView):
    """
    Weekly summary
    """
    model = Compra
    template_name =  'compras/resumen_semanal.html'
    context_object_name = 'resumen'
    
    def get_queryset(self):
        hace_una_semana = timezone.now() - timedelta(days=60)
        return (Compra.objects.filter(fecha__gte=hace_una_semana)
            .values('producto__almacen__nombre', 'producto__nombre', 'fecha')
            .annotate(
                total_comprado=Sum('cantidad'),
                gasto_total=Sum(F('cantidad') * F('precio_compra'))
            )
            # .order_by('producto__almacen__nombre'))
            .order_by('fecha'))


class ResumenProductoSemanalView(ListView):
    """
    Weekly product summary
    """
    model = Compra
    template_name = 'compras/resumen_productossemanal.html'
    context_object_name = 'resumen'

    def get_queryset(self):
        hace_una_semana = timezone.now() - timedelta(days=60)
        return (Compra.objects.filter(fecha__gte=hace_una_semana)
            .values('producto__almacen__nombre', 'fecha')
            .annotate(
                total_comprado=Sum('cantidad'),
                gasto_total=Sum(F('cantidad') * F('precio_compra'))
            )
            .order_by('fecha'))


class ResumenSemanalLecheView(View):
    """
    Weekly milk product sumary
    """
    def get(self, request):
        resumen = None
        return render(
            request,
            'compras/resumen_productolechessemanal.html', 
            {'resumen': resumen}
            )

 
    def post(self, request):
        form = ResumenSemanal(request.POST)
        resumen = None
        # print(f"Lo que llega del formulario POST: {form}")
        if form.is_valid():
            llega = form.cleaned_data['datefilter']
            fecha_informal= llega.split(' - ')
            # print(f"Fecha informal: {fecha_informal}")
            desde= fecha_informal[0]
            hasta = fecha_informal[1]
            resumen = Compra.objects.filter(
                fecha__range=[desde, hasta],
                producto__almacen__nombre='Leche'
            ).order_by('fecha')
            largo = len(resumen)
            fechas = []
            for f in resumen:
                if f.fecha not in fechas:
                    fechas.append(f.fecha)

            #ordenados = sorted(resumen, key=lambda index : index[2])
            # sorted(resumen, key=itemgetter('fecha'))
            listado = []
            fila = {}
            a = 1
            cant = 0
            canti = []
            nombre = []
            comparar = True
            total_litros = 0
            totales_apagar = 0 
            # print("listado el resumen")
            for l in resumen:
                # fila['no'] = a
                if l.producto not in nombre:
                    nombre.append(l.producto)
                    fila['nombre'] = l.producto
                    f = 0
                    for p in resumen:
                        if l.producto == p.producto:
                            # print('voy dentro del While')
                            while comparar:
                                # print(f"Comparando {p.producto} si fechas[f] {fechas[f]} == p.fecha: {p.fecha}")
                                if fechas[f] == p.fecha:
                                    canti.append(p.cantidad)
                                    cant += p.cantidad
                                    # print("coinciden")
                                    comparar = False
                                else:
                                    canti.append(0)
                                    # print("no coinciden")
                                    f += 1
                            f += 1
                            comparar = True
                    if len(fechas) != f:
                        canti.append(0)
                    fila['cantidad'] = canti
                    # print(f" f se quedó en: {f} y tamaño fechas {len(fechas)}")
                    canti = []
                    if cant != 0:
                        fila['cant'] = cant
                        fila['precio'] = l.precio_compra
                        fila['apagar'] = cant * l.precio_compra
                        listado.append(fila)
                        total_litros += fila['cant']
                        totales_apagar += fila['apagar']
                a += 1
                fila = {}
                cant = 0

            total_litros_dias = (Compra.objects.filter(fecha__range=[desde, hasta])
                .values('producto__almacen__nombre', 'fecha')
                .annotate(
                    total_comprado=Sum('cantidad'),
                    gasto_total=Sum(F('cantidad') * F('precio_compra'))
                )
                .order_by('fecha'))

            # print(f"resultado de la búsquda: {resumen}, largo de la búsquda: {largo}")
            # print(f"las fechas en el arreglo: {fechas}")
            # print("resume sale así: ", resumen)
            # print("resume sale así: ")
            # print("El listado está: ")
            # print(np.matrix(listado))
            # print(np.matrix(resumen))
            # print(f"total litros dias: {total_litros_dias}")


        return render(
            request,
            'compras/resumen_productolechessemanal.html', 
            {
                'resumen': resumen,
                'fechas': fechas,
                'listado': listado,
                'totales_apagar': totales_apagar,
                'total_litros': total_litros,
                'total_litros_dias': total_litros_dias,
            }
        )


# Vistas para Clientes
class ClienteListView(ListView):
    """
    Vista para lisrar Clientes de la Facturación
    """
    model = Cliente
    template_name = 'facturas/cliente_list.html'
    context_object_name = 'clientes'


class ClienteDetailView(DetailView):
    """
    Vista para el detalle de un Cliente de la Facturación
    """
    model = Cliente
    template_name = 'facturas/cliente_detail.html'
    context_object_name = 'cliente'


class ClienteCreateView(CreateView):
    """
    Vista para crear un Cliente de la Facturación
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'facturas/cliente_form.html'
    success_url = reverse_lazy('cliente_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente creado exitosamente.")
        return super().form_valid(form)


class ClienteUpdateView(UpdateView):
    """
    Vista para actualizar un Cliente de la Facturación
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'facturas/cliente_form.html'
    success_url = reverse_lazy('cliente_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado exitosamente.")
        return super().form_valid(form)


class ClienteDeleteView(DeleteView):
    """
    Vista para borrar un Cliente de la Facturación
    """
    model = Cliente
    template_name = 'facturas/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Productos
class ProductoListView(ListView):
    """
    Vista para listar los Productos de la Facturación
    """
    model = Producto
    template_name = 'facturas/producto_list.html'
    context_object_name = 'productos'


class ProductoDetailView(DetailView):
    """
    Vista para el Detalle de un Productos de la Facturación
    """
    model = Producto
    template_name = 'facturas/producto_detail.html'
    context_object_name = 'producto'


class ProductoCreateView(CreateView):
    """
    Vista para crear un Producto de la Facturación
    """
    model = Producto
    form_class = ProductoForm
    template_name = 'facturas/producto_form.html'
    success_url = reverse_lazy('producto_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)


class ProductoUpdateView(UpdateView):
    """
    Vista para actualizar el Producto de la Facturación
    """
    model = Producto
    form_class = ProductoForm
    template_name = 'facturas/producto_form.html'
    success_url = reverse_lazy('producto_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)


class ProductoDeleteView(DeleteView):
    """
    Vista para borrar un producto de la Facturación
    """
    model = Producto
    template_name = 'facturas/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Facturas
class FacturaListView(ListView):
    """
    Vista para listar la Factura
    """
    model = Factura
    template_name = 'facturas/factura_list.html'
    context_object_name = 'facturas'
    ordering = ['-fecha_emision']


class FacturaDetailView(DetailView):
    """
    Vista Detalle del Detalle de la Factura
    """
    model = Factura
    template_name = 'facturas/factura_detail.html'
    context_object_name = 'factura'


# @login_required
def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                factura = form.save()
                formset = DetalleFacturaFormSet(request.POST, instance=factura)
                
                if formset.is_valid():
                    formset.save()
                    factura.calcular_totales()
                    messages.success(request, "Factura creada exitosamente.")
                    return redirect('factura_detail', pk=factura.pk)
                else:
                    # Si el formset no es válido, eliminamos la factura
                    factura.delete()
    else:
        form = FacturaForm()
        formset = DetalleFacturaFormSet()
    
    return render(request, 'facturas/factura_form.html', {
        'form': form,
        'formset': formset,
    })


# @login_required
def editar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    
    if factura.estado != 'pendiente':
        messages.error(request, "No se puede editar una factura que no esté en estado pendiente.")
        return redirect('factura_detail', pk=factura.pk)
    
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            with transaction.atomic():
                factura = form.save()
                formset = DetalleFacturaFormSet(request.POST, instance=factura)
                
                if formset.is_valid():
                    formset.save()
                    factura.calcular_totales()
                    messages.success(request, "Factura actualizada exitosamente.")
                    return redirect('factura_detail', pk=factura.pk)
    else:
        form = FacturaForm(instance=factura)
        formset = DetalleFacturaFormSet(instance=factura)
    
    return render(request, 'facturas/factura_form.html', {
        'form': form,
        'formset': formset,
        'factura': factura,
    })


# @login_required
def cambiar_estado_factura(request, pk, estado):
    factura = get_object_or_404(Factura, pk=pk)
    estados_validos = [e[0] for e in Factura.ESTADO_CHOICES]
    
    if estado not in estados_validos:
        messages.error(request, "Estado no válido.")
    else:
        factura.estado = estado
        factura.save()
        messages.success(request, f"Estado de factura cambiado a {estado}.")
    
    return redirect('factura_detail', pk=factura.pk)


# @login_required
def eliminar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    
    if request.method == 'POST':
        factura.delete()
        messages.success(request, "Factura eliminada exitosamente.")
        return redirect('factura_list')
    
    return render(request, 'facturas/factura_confirm_delete.html', {
        'factura': factura,
    })


# API para obtener información de productos
def get_producto_info(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            producto = Producto.objects.get(pk=request.GET['id'])
            data = {
                'precio': float(producto.precio),
                'stock': producto.stock,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Producto.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Producto no encontrado'}), content_type='application/json')
    
    return HttpResponse(json.dumps({'error': 'Solicitud inválida'}), content_type='application/json')