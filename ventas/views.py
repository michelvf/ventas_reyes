import pandas as pd
import chardet
import csv
import datetime
from django.shortcuts import render
from .forms import ExcelUploadForm
from django.views.generic.edit import FormView
from rest_framework.views import APIView
from django.views.generic import TemplateView
from .models import Departamentos, Productos, Ventas, fileUpdate
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy

from django.views import View
from django.http import HttpResponse



# Index Page
class IndexView(TemplateView):
    template_name = 'ventas/index.html'
    # template_name = 'ventas/index2.html'


# Create your views here.
class ExcelUploadView(FormView):
    """
    Vista para subir los ficheros Excel e insertarlos en al Base de Datos
    """
    template_name = 'ventas/upload.html'
    # template_name = 'ventas/subir.html'
    form_class = ExcelUploadForm
    success_url = '/ventas/success/'
    # success_url = reverse_lazy('success')

    # def get(self, request):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request):
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         excel_file = request.FILES['file']
    #         try:
    #             df = pd.read_excel(excel_file)
    #             # Aquí puedes realizar más validaciones o procedimientos con el DataFrame
    #             return HttResponse("Archivo leído correctamante")
    #         except Exception as e:
    #             error_message = f"Error al leer el fichero: {e}"
    #             return render(request, self.template_name, {'form': form, 'error': error_message})
    #     return render(request, self.template_name, {'form': form})



    def form_valid(self, form):
        """
        Obtener el fichero y fecha, y registrar sus datos en la Base de Datos
        """
        # Obteniendo los valores del formulario
        date = form.cleaned_data['datefilter']
        file = form.cleaned_data['file']
        actualizar = form.cleaned_data['actualizar']
        # print(f"Llegó del forumario: date: ", date, ", file: ", file, ", actualizar: ", actualizar)

        try:
            # Leer el fichero recibido
            raw_data = file.read()

            # Con Pandas leer el fichero exel
            excel_file = pd.read_excel(file)
            # excel_file = pd.read_excel(file, encoding='ISO-8859-1')
            # wb = xlrd.open_workbook(file, encoding_override='CORRECT_ENCODING')
            # excel_file = pd.read_excel(file, engine='calamine')
        except Exception as e:
            form.add_error('file', 'Error al leer el fichero, debe convertirlo a fichero de excel como indica la figura: {}'.format(e))
            return self.form_invalid(form)
        
        # Insertando los Departamentos
        for i in range(len(excel_file['Departamento'])):

            # Tomando el valor de un departamento
            departamento = excel_file['Departamento'][i]

            # Verificando si existe en la BD e insertarlo si no existe
            if not Departamentos.objects.filter(departamento=departamento).exists():
                # print(f"no existe: {departamento}, se agrega")
                # Preparado para insertarlo en el modelo Departamento
                obj = Departamentos(
                    departamento=departamento,
                )
                # Guardando en la BD
                obj.save()


        # Insertando los Productos
        for i in range(len(excel_file['Descripcion'])):

            # Tomando el valor de un departamento
            producto = excel_file['Descripcion'][i]
            codigo = excel_file['Codigo'][i]
            departamento=Departamentos.objects.get(departamento=excel_file['Departamento'][i])

            # Verificando si existe en la BD e insertarlo si no existe
            if not Productos.objects.filter(codigo=codigo).exists():
                # Preparado para insertarlo en el modelo Departamento
                obj = Productos(
                    codigo=codigo,
                    producto=producto,
                    id_departamento=departamento
                )
                # Guardando en la BD
                obj.save()

        # Borrar los que se van a actualizar
        if actualizar:
            ventas = Ventas.objects.filter(fecha=date).delete()
            # print(f"se van a borrar: {ventas}")
        else:
            fileUp = fileUpdate(fecha=date)
            fileUp.save()

        # Insertando las Ventas
        for i in range(len(excel_file)):
            # Leyendo una fila
            fila = excel_file.iloc[i]
            
            # Buscando el id del producto a insertar
            codigo_venta = Productos.objects.get(codigo=fila['Codigo'])
            # Tomando valores del Excel
            cantidad = float(fila['Cantidad'])
            venta = float(fila['Precio Usado'])
            costo = float(fila['Precio Costo'])
            calculo = (venta - costo) * cantidad
            # Buscando el valor del id del Departamento de la venta
            # departamento_venta = Departamentos.objects.get(departamento=fila['Departamento'])
            # Tomando la fecha que se insertó
            fecha = date

            # Preparado para insertarlo en el modelo Departamento
            obj_venta = Ventas(
                id_producto=codigo_venta,
                cantidad=cantidad,
                venta=venta,
                costo=costo,
                calculo=calculo,
                # departamento=departamento_venta,
                fecha=fecha
            )
            # Guardando en la BD
            # print(f"Se va a guardar: {obj_venta}")
            obj_venta.save()

        # return JsonResponse({'mensaje': 'Datos recibidos correctamente!'})
        messages.success(self.request, 'Fichero subido y leído correctamente')
        return super().form_valid(form)


    def form_invalid(self, form):
        # return JsonResponse({'error': 'Datos no válidos'}, status=400) 
        messages.error(self.request, 'Fichero ha dando error al leerlo.')
        response = super().form_invalid(form)

        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)


class ShowVentas(TemplateView):
    """
    Show the Ventas with DataTables JS
    """
    template_name = 'ventas/ventas.html'


class ShowDepartamentos(TemplateView):
    """
    Show the Departamentos with DataTables JS
    """
    template_name = 'ventas/departamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["URL"] = "/api/departamentos/"
        
        return context
    


class ShowProductos(TemplateView):
    """
    Show the Productos with DataTables JS
    """
    template_name = 'ventas/productos.html'


class ShowEntreFechas(TemplateView):
    """
    Show the Sales bettwen two dates
    """
    template_name = 'ventas/entre_fechas.html'


class SumarPorFechas(TemplateView):
    """
    Show the Sum of sales bettewn tow dates
    """
    template_name = 'ventas/suma_por_fechas.html'


class ProdxDepto(TemplateView):
    """
    Show productos por Departamentos
    """
    template_name = 'ventas/productos_x_depto.html'


class ProdMasVendido(TemplateView):
    """
    Show the products more sales
    """
    template_name = 'ventas/produtos_mas_vendido.html'


class LacteosVendidos(TemplateView):
    """
    Show the lacteos more sales
    """
    template_name = 'ventas/lacteos.html'


class ListadoFicherosSubidos(TemplateView):
    """
    Show the files uploaded
    """
    template_name = 'ventas/ficherosSubidos.html'

"""
Punto la Parada:
21.73781, -82.75416

Punto Di MUU
21.74459, -82.75517
"""