from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views import View
from django.utils import timezone
from django.db.models import Sum, F, Count
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy, reverse
from datetime import timedelta
from .models import Almacen, Producto, Compra, PrecioProducto, UnidadMedida
from .forms import CompraForm, AlmacenForm, ProductoForm, PrecioProductoForm
from .forms import ResumenSemanal
from rest_framework import authentication
from operator import itemgetter, attrgetter
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from .models import Cliente, Producto, Factura, DetalleFactura
from .forms import ClienteForm, ProductoForm, FacturaForm, DetalleFacturaFormSet
from .forms import UnidadMedidaForm

def factura_pdf(request, pk):
    """Generate PDF for a specific invoice"""
    factura = get_object_or_404(Factura, pk=pk)
    template_path = 'facturas/Factura.html'
    
    # Get the context data
    context = {
        'factura': factura,
        'request': request,
    }
    
    # Render the template with the context
    template = get_template(template_path)
    html = template.render(context)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero}.pdf"'
    
    # Create PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response,
    )
    
    # If error then show some funny view
    if pisa_status.err:
        return HttpResponse('Temenos algún error <pre>' + html + '</pre>')
    return response


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


# Vista Unidad de Medida
class UnidadMedidaListView(ListView):
    """
    Vista para listar las Unidades de Medida de la Facturación
    """
    model = UnidadMedida
    template_name = 'facturas/unidadmedida_list.html'
    context_object_name = 'unidad_medidas'


class UnidadMedidaCreateView(CreateView):
    """
    Vista para crear las Unidades de Medida de la Facturación
    """
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'facturas/unidadmedida_form.html'
    success_url = reverse_lazy('unidadmedida_list')


class UnidadMedidaDetailView(DetailView):
    """
    Vista para el detalle de la Unidad de Medida de la Facturación
    """
    model = UnidadMedida
    template_name = 'facturas/unidadmedida_detail.html'
    context_object_name = 'unidad_medidas'


class UnidadMedidaUpdateView(UpdateView):
    """
    Vista para actualizar un Unidad Medida de la Facturación
    """
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'facturas/unidadmedida_form.html'
    success_url = reverse_lazy('unidadmedida_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Unidad Medida actualizado exitosamente.")
        return super().form_valid(form)


class UnidadMedidaDeleteView(DeleteView):
    """
    Vista para borrar un Unidad Medida de la Facturación
    """
    model = UnidadMedida
    template_name = 'facturas/unidadmedida_confirm_delete.html'
    success_url = reverse_lazy('unidadmedida_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Unidad Medida eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


# Vistas para Clientes
class ClienteListView(ListView):
    """
    Vista para listar Clientes de la Facturación
    """
    model = Cliente
    template_name = 'facturas/cliente_list.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        """
        Anota el total facturado para cada cliente.
        """
        return Cliente.objects.annotate(
            total_facturado=Coalesce(Sum('facturas__total'), 0.00)
        ).order_by('nombre', 'apellido')


class ClienteDetailView(DetailView):
    """
    Vista para el detalle de un Cliente de la Facturación
    """
    model = Cliente
    template_name = 'facturas/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optimizar la consulta de facturas para evitar múltiples consultas en la plantilla
        context['facturas'] = self.object.facturas.all().select_related('cliente').order_by('-fecha_emision')
        return context


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

    def get_queryset(self):
        """
        Anota el total facturado para cada cliente.
        """
        return Producto.objects.annotate(
            total_facturado=Count('detallefactura__factura__id', distinct=True)
        )


class ProductoDetailView(DetailView):
    """
    Vista para el Detalle de un Productos de la Facturación
    """
    model = Producto
    template_name = 'facturas/producto_detail.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.object
        # Optimizar la consulta de facturas para evitar múltiples consultas en la plantilla
        # context['facturas'] = self.object.detallefactura.all().select_related('producto').order_by('-fecha_emision')
        # Obtener facturas únicas donde aparece el producto
        facturas = Factura.objects.filter(detalles__producto=producto).distinct()

        context['facturas'] = facturas
        return context


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


# Clase personalizada para serializar Decimal a JSON
class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


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
                    # return redirect('factura_detail', pk=factura.pk)
                    return redirect('ver_factura', pk=factura.pk)
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
    
    if factura.estado != 'pendiente' and factura.estado != 'pagada':
        messages.error(request, "No se puede editar una factura que no esté en estado pendiente.")
        # return redirect('factura_detail', pk=factura.pk)
        return redirect('ver_factura', pk=factura.pk)

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
                    # return redirect('factura_detail', pk=factura.pk)
                    return redirect('ver_factura', pk=factura.pk)
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
        # Mensaje personalizado según el estado
        if estado == 'pagada':
            messages.success(request, "Factura marcada como pagada.")
        elif estado == 'pagada-eleventa':
            messages.success(request, "Factura marcada como pagada en Eleventa.")
        elif estado == 'anulada':
            messages.success(request, "Factura anulada correctamente.")
        else:
            messages.success(request, f"Estado de factura cambiado a {estado}.")

    
    return redirect('ver_factura', pk=factura.pk)


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


# API para obtener facturas actualizadas
def get_facturas_json(request):
    facturas = Factura.objects.all().order_by('-fecha_emision')
    
    data = []
    for factura in facturas:
        # Determinar el HTML del estado para mantener consistencia con la vista
        if factura.estado == 'pendiente':
            estado_html = '<span class="badge bg-warning">Pendiente</span>'
        elif factura.estado == 'pagada':
            estado_html = '<span class="badge bg-info">Pagada</span>'
        elif factura.estado == 'pagada-eleventa':
            estado_html = '<span class="badge bg-success">Pagada en Eleventa</span>'
        else:
            estado_html = '<span class="badge bg-danger">Anulada</span>'
        
        # Generar HTML para los botones de acción
        acciones_html = f'''
        <div class="btn-group" role="group">
            <a href="{reverse('ver_factura', args=[factura.id])}" class="btn btn-sm btn-info">
                <i class="fas fa-eye"></i>
            </a>
        '''
        
        if factura.estado == 'pendiente':
            acciones_html += f'''
            <a href="{reverse('factura_update', args=[factura.id])}" class="btn btn-sm btn-warning">
                <i class="fas fa-edit"></i>
            </a>
            '''
            
        acciones_html += f'''
            <a href="{reverse('factura_delete', args=[factura.id])}" class="btn btn-sm btn-danger">
                <i class="fas fa-trash"></i>
            </a>
        </div>
        '''
        
        data.append({
            'DT_RowId': f'factura-{factura.id}',
            'numero': factura.numero,
            'cliente': f"{factura.cliente.nombre} {factura.cliente.apellido}",
            'fecha': {
                'display': factura.fecha_emision.strftime("%d/%m/%Y %H:%M"),
                'timestamp': factura.fecha_emision.timestamp()
            },
            'total': {
                'display': f"$ {factura.total}",
                'value': float(factura.total)
            },
            'estado': {
                'display': estado_html,
                'value': factura.estado
            },
            'acciones': acciones_html
        })
    
    return JsonResponse({'data': data})


# API para obtener facturas de un cliente específico
def get_facturas_cliente_json(request, cliente_id):
    """
    Mostrar las Facturas que tiene el Cliente
    """
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    facturas = cliente.facturas.all().order_by('-fecha_emision')
    
    data = []
    for factura in facturas:
        # Determinar el HTML del estado
        if factura.estado == 'pendiente':
            estado_html = '<span class="badge bg-warning">Pendiente</span>'
        elif factura.estado == 'pagada':
            estado_html = '<span class="badge bg-info">Pagada</span>'
        elif factura.estado == 'pagada-eleventa':
            estado_html = '<span class="badge bg-success">Pagada en Eleventa</span>'
        else:
            estado_html = '<span class="badge bg-danger">Anulada</span>'
        
        data.append({
            'DT_RowId': f'factura-cliente-{factura.id}',
            'numero': factura.numero,
            'fecha': {
                'display': factura.fecha_emision.strftime("%d/%m/%Y"),
                'timestamp': factura.fecha_emision.timestamp()
            },
            'cantidad_producto': {
                'display': factura.cantidad_producto,
                'value': factura.cantidad_producto,
            },
            'total': {
                'display': f"$ {factura.total}",
                'value': float(factura.total)
            },
            'estado': {
                'display': estado_html,
                'value': factura.estado
            },
            'acciones': f'''
            <a href="{reverse('ver_factura', args=[factura.id])}" class="btn btn-sm btn-info">
                <i class="fas fa-eye"></i>
            </a>
            '''
        })
    
    return JsonResponse({'data': data})


def get_facturas_productos_json(request, producto_id):
    """
    Mostrar las Facturas donde aparece el producto
    """
    print(f"buscar producto: {producto_id}")

    producto = get_object_or_404(Producto, pk=producto_id)
    facturas = Factura.objects.filter(detalles__producto_id=producto_id).distinct().order_by('fecha_emision')
    # facturas = producto.detalles.facturas.all().order_by('-fecha_emision')
    
    data = []
    for factura in facturas:
        # Determinar el HTML del estado
        if factura.estado == 'pendiente':
            estado_html = '<span class="badge bg-warning">Pendiente</span>'
        elif factura.estado == 'pagada':
            estado_html = '<span class="badge bg-info">Pagada</span>'
        elif factura.estado == 'pagada-eleventa':
            estado_html = '<span class="badge bg-success">Pagada en Eleventa</span>'
        else:
            estado_html = '<span class="badge bg-danger">Anulada</span>'
        
        data.append({
            'DT_RowId': f'factura-cliente-{factura.id}',
            'numero': factura.numero,
            'fecha': {
                'display': factura.fecha_emision.strftime("%d/%m/%Y"),
                'timestamp': factura.fecha_emision.timestamp()
            },
            'cantidad_producto': {
                'display': factura.cantidad_producto,
                'value': factura.cantidad_producto,
            },
            'total': {
                'display': f"$ {factura.total}",
                'value': float(factura.total)
            },
            'estado': {
                'display': estado_html,
                'value': factura.estado
            },
            'acciones': f'''
            <a href="{reverse('ver_factura', args=[factura.id])}" class="btn btn-sm btn-info">
                <i class="fas fa-eye"></i>
            </a>
            '''
        })
    
    return JsonResponse({'data': data})


class VerFactura(DetailView):
    """
    Ver la factura que hizo la IA
    """
    model = Factura
    template_name = "facturas/Factura.html"
    context_object_name = 'factura'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.cantidad_producto < 8:
            columnas = 13 - self.object.cantidad_producto
            context["columnas"] = range(columnas)
        else:
            context["columnas"] = None
        
        return context


class APIProductos(View):
    """
    API Productos para la Factura
    """
    def get(self, request):
        productos = Producto.objects.select_related('unidadmedida').all()
        data = []

        for producto in productos:
            data.append({
                "id": producto.id,
                "producto": producto.nombre,
                "codigo": producto.codigo,
                "descripcion": producto.descripcion,
                "unidad_medida": {
                    "nombre": producto.unidadmedida.nombre,
                    "sigla": producto.unidadmedida.sigla,
                },
            })

        return JsonResponse(data, safe=False)


class PruebaBT(TemplateView):
    """Probando Bootstrap Table View"""
    template_name = "compras/bt.html"
