from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, F

from .models import Producto, Material, ProcesoProduccion, EntradaProduccion
from .forms import ProductoForm, MaterialForm, ProcesoProduccionForm, EntradaProduccionForm


# Dashboard
# class DashboardView(LoginRequiredMixin, TemplateView):
class DashboardView(TemplateView):
    template_name = 'produc_proceso/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_count'] = Producto.objects.count()
        context['procesos_activos'] = ProcesoProduccion.objects.exclude(estado='finalizado').exclude(estado='cancelado').count()
        context['procesos_recientes'] = ProcesoProduccion.objects.order_by('-fecha_inicio')[:5]
        
        # Productos con mayor costo acumulado
        productos = Producto.objects.all()
        productos_con_costo = [(p, p.costo_total()) for p in productos]
        productos_con_costo.sort(key=lambda x: x[1], reverse=True)
        context['productos_top'] = productos_con_costo[:5]
        
        return context


# Vistas de Productos
# class ProductoListView(LoginRequiredMixin, TemplateView):
class ProductoListView(TemplateView):
    template_name = 'produc_proceso/producto_lista.html'


# class ProductoAPIView(LoginRequiredMixin, View):
class ProductoAPIView(View):
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        data = []
        
        for producto in productos:
            costo_total = producto.costo_total()
            margen = producto.margen_ganancia()
            
            data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion or '',
                'precio_venta': float(producto.precio_venta),
                'costo_total': float(costo_total),
                'margen': float(margen),
            })
        
        return JsonResponse({'data': data})


# class ProductoDetailView(LoginRequiredMixin, DetailView):
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'produc_proceso/producto_detalle.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.get_object()
        context['procesos'] = ProcesoProduccion.objects.filter(producto=producto).order_by('-fecha_inicio')
        context['costo_total'] = producto.costo_total()
        context['margen'] = producto.margen_ganancia()
        return context


# class ProductoCreateView(LoginRequiredMixin, CreateView):
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'produc_proceso/producto_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Producto'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Producto creado correctamente.')
        return reverse_lazy('produccion:producto_lista')


# class ProductoUpdateView(LoginRequiredMixin, UpdateView):
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'produc_proceso/producto_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Producto actualizado correctamente.')
        return reverse_lazy('produccion:producto_detalle', kwargs={'pk': self.object.pk})


# Vistas de Materiales
# class MaterialListView(LoginRequiredMixin, ListView):
class MaterialListView(ListView):
    model = Material
    template_name = 'produc_proceso/material_lista.html'
    context_object_name = 'materiales'
    ordering = ['nombre']


# class MaterialCreateView(LoginRequiredMixin, CreateView):
class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'produc_proceso/material_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Material'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Material creado correctamente.')
        return reverse_lazy('produccion:material_lista')


# class MaterialUpdateView(LoginRequiredMixin, UpdateView):
class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'produc_proceso/material_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Material'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Material actualizado correctamente.')
        return reverse_lazy('produccion:material_lista')


# Vistas de Procesos de Producción
# class ProcesoListView(LoginRequiredMixin, TemplateView):
class ProcesoListView(TemplateView):

    template_name = 'produc_proceso/proceso_lista.html'


# class ProcesoAPIView(LoginRequiredMixin, View):
class ProcesoAPIView(View):
    def get(self, request, *args, **kwargs):
        procesos = ProcesoProduccion.objects.all().order_by('-fecha_inicio')
        data = []
        
        for proceso in procesos:
            data.append({
                'id': proceso.id,
                'producto': proceso.producto.nombre,
                'fecha_inicio': proceso.fecha_inicio.strftime('%Y-%m-%d'),
                'fecha_fin': proceso.fecha_fin.strftime('%Y-%m-%d') if proceso.fecha_fin else '',
                'estado': dict(ProcesoProduccion._meta.get_field('estado').choices).get(proceso.estado),
                'costo_total': float(proceso.costo_total()),
            })
        
        return JsonResponse({'data': data})


# class ProcesoDetailView(LoginRequiredMixin, DetailView):
class ProcesoDetailView(DetailView):
    model = ProcesoProduccion
    template_name = 'produc_proceso/proceso_detalle.html'
    context_object_name = 'proceso'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proceso = self.get_object()
        context['costo_total'] = proceso.costo_total()
        return context


# class ProcesoCreateView(LoginRequiredMixin, CreateView):
class ProcesoCreateView(CreateView):
    model = ProcesoProduccion
    form_class = ProcesoProduccionForm
    template_name = 'produc_proceso/proceso_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Proceso de Producción'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Proceso de producción creado correctamente.')
        return reverse_lazy('produccion:proceso_detalle', kwargs={'pk': self.object.pk})


# class ProcesoUpdateView(LoginRequiredMixin, UpdateView):
class ProcesoUpdateView(UpdateView):
    model = ProcesoProduccion
    form_class = ProcesoProduccionForm
    template_name = 'produc_proceso/proceso_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proceso de Producción'
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Proceso de producción actualizado correctamente.')
        return reverse_lazy('produccion:proceso_detalle', kwargs={'pk': self.object.pk})


# class ProcesoFinalizarView(LoginRequiredMixin, View):
class ProcesoFinalizarView(View):
    def get(self, request, *args, **kwargs):
        proceso = get_object_or_404(ProcesoProduccion, pk=kwargs['pk'])
        
        if proceso.estado not in ['finalizado', 'cancelado']:
            proceso.estado = 'finalizado'
            proceso.fecha_fin = timezone.now().date()
            proceso.save()
            messages.success(request, 'Proceso de producción finalizado correctamente.')
        
        return redirect('produccion:proceso_detalle', pk=proceso.pk)


# Vistas de Entradas de Producción
# class EntradaAPIView(LoginRequiredMixin, View):
class EntradaAPIView(View):
    def get(self, request, *args, **kwargs):
        proceso_id = kwargs['proceso_id']
        entradas = EntradaProduccion.objects.filter(proceso_id=proceso_id).order_by('-fecha')
        data = []
        
        for entrada in entradas:
            data.append({
                'id': entrada.id,
                'material': entrada.material.nombre,
                'cantidad': float(entrada.cantidad),
                'unidad': entrada.material.unidad_medida,
                'costo_unitario': float(entrada.material.costo_unitario),
                'costo_total': float(entrada.costo()),
                'fecha': entrada.fecha.strftime('%Y-%m-%d'),
            })
        
        return JsonResponse({'data': data})


# class EntradaCreateView(LoginRequiredMixin, CreateView):
class EntradaCreateView(CreateView):
    model = EntradaProduccion
    form_class = EntradaProduccionForm
    template_name = 'produc_proceso/entrada_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.proceso = get_object_or_404(ProcesoProduccion, pk=kwargs['proceso_id'])
        
        if self.proceso.estado in ['finalizado', 'cancelado']:
            messages.error(request, 'No se pueden agregar entradas a un proceso finalizado o cancelado.')
            return redirect('produccion:proceso_detalle', pk=self.proceso.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Entrada de Producción'
        context['proceso'] = self.proceso
        return context
    
    def form_valid(self, form):
        form.instance.proceso = self.proceso
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Entrada de producción registrada correctamente.')
        return reverse_lazy('produccion:proceso_detalle', kwargs={'pk': self.proceso.pk})


# class EntradaUpdateView(LoginRequiredMixin, UpdateView):
class EntradaUpdateView(UpdateView):
    model = EntradaProduccion
    form_class = EntradaProduccionForm
    template_name = 'produc_proceso/entrada_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.proceso.estado in ['finalizado', 'cancelado']:
            messages.error(request, 'No se pueden editar entradas de un proceso finalizado o cancelado.')
            return redirect('produccion:proceso_detalle', pk=self.object.proceso.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Entrada de Producción'
        context['proceso'] = self.object.proceso
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'Entrada de producción actualizada correctamente.')
        return reverse_lazy('produccion:proceso_detalle', kwargs={'pk': self.object.proceso.pk})


# class EntradaDeleteView(LoginRequiredMixin, View):
class EntradaDeleteView(View):
    def get(self, request, *args, **kwargs):
        entrada = get_object_or_404(EntradaProduccion, pk=kwargs['pk'])
        proceso_id = entrada.proceso.pk
        
        if entrada.proceso.estado in ['finalizado', 'cancelado']:
            messages.error(request, 'No se pueden eliminar entradas de un proceso finalizado o cancelado.')
        else:
            entrada.delete()
            messages.success(request, 'Entrada de producción eliminada correctamente.')
        
        return redirect('produccion:proceso_detalle', pk=proceso_id)
