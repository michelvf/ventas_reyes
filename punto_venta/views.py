from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Producto, Transaccion, Venta, DetalleVenta, Cliente
from .forms import VentaForm, DetalleVentaForm
from django.views import View
from django.utils import timezone
from datetime import datetime
from django.forms import inlineformset_factory


# Create your views here.

class ProductoListView(ListView):
    model = Producto
    template_name = 'punto_venta/producto_list.html'
    context_object_name = 'productos'


class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'punto_venta/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'cantidad']
    success_url = reverse_lazy('producto_list')


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'punto_venta/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'cantidad']
    success_url = reverse_lazy('producto_list')


class TransaccionCreateView(CreateView):
    model = Transaccion
    template_name = 'punto_venta/transaccion_form.html'
    fields = ['producto', 'tipo', 'cantidad']
    success_url = reverse_lazy('transaccion_list')


class DashboardView(View):
   template_name = 'punto_venta/dashboard.html'

   def get(self, request, *args, **kwargs):
       productos = Producto.objects.all()
       transacciones = Transaccion.objects.all()
       return render(request, self.template_name, {
           'productos': productos,
           'transacciones': transacciones,
       })


class TransaccionListView(ListView):
    model = Transaccion
    template_name = 'punto_venta/transaccion_list.html'
    context_object_name = 'transacciones'

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class ExistenciaMensualView(View):
    template_name = 'punto_venta/existencia_mensual.html'

    def get(self, request, *args, **kwargs):
        año = request.GET.get('año', timezone.now().year)
        mes = request.GET.get('mes', timezone.now().month)
        transacciones = Transaccion.objects.filter(fecha__year=año, fecha__month=mes)

        existencia = {}

        for transaccion in transacciones:
            producto = transaccion.producto
            if producto not in existencia:
                existencia[producto] = 0
            if transaccion.tipo == 'entrada':
                existencia[producto] += transaccion.cantidad

            else:
                existencia[producto] -= transaccion.cantidad
                
        return render(request, self.template_name, {
            'existencia': existencia,
            'año': año,
            'mes': mes,
        })


class VentaCreateView(View):
    def get(self, request, *args, **kwargs):
        venta_form = VentaForm()
        detalle_venta_formset = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=1)
        formset = detalle_venta_formset()
        return render(request, 
            'punto_venta/venta_form.html', 
            {'venta_form': venta_form, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        venta_form = VentaForm(request.POST)
        detalle_venta_formset = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=1)
        formset = detalle_venta_formset(request.POST)

        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.venta = venta
                detalle.save()
            return redirect('venta_list')
        return render(request,
            'punto_venta/venta_form.html',
            {'venta_form': venta_form, 'formset': formset}
        )


class VentaList(ListView):
    model = Venta
    template_name = 'punto_venta/venta_list.html'
    context_object_name = 'ventas'


class DetalleVentaList(ListView):
    model = DetalleVenta
    template_name = 'punto_venta/detalle_venta_list.html'
    context_object_name = 'detalle_ventas'


class ClienteList(ListView):
    model = Cliente
    template_name = 'punto_venta/cliente_list.html'
    context_object_name = 'clientes'
