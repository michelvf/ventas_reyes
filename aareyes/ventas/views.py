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
    form_class = ExcelUploadForm
    success_url = '/ventas/success/'


    def form_valid(self, form):
        """
        Obtener el fichero y fecha, y registrar sus datos en la Base de Datos
        """
        # Obteniendo los valores del formulario
        date = form.cleaned_data['datefilter']
        file = form.cleaned_data['file']
        actualizar = form.cleaned_data['actualizar']
        print(f"Llegó del forumario: date: ", date, ", file: ", file, ", actualizar: ", actualizar)

        # Leer el fichero recibido
        raw_data = file.read()

        # Con Pandas leer el fichero exel
        excel_file = pd.read_excel(file)
        # excel_file = pd.read_excel(file, encoding='ISO-8859-1')
        # wb = xlrd.open_workbook(file, encoding_override='CORRECT_ENCODING')
        # excel_file = pd.read_excel(file, engine='calamine')
        
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

            return JsonResponse({'mensaje': 'Datos recibidos correctamente!'})

        # return super().form_valid(form)
    def form_invalid(self, form):
        return JsonResponse({'error': 'Datos no válidos'}, status=400) 


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


class LacreosVendidos(TemplateView):
    """
    Show the lacteos more sales
    """
    template_name = 'ventas/lacteos.html'