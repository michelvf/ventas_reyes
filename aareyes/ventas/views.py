import pandas as pd
import chardet
import csv
import datetime
from django.shortcuts import render
from .forms import ExcelUploadForm
from django.views.generic.edit import FormView
from rest_framework.views import APIView
from django.views.generic import TemplateView
from .models import Departamentos, Productos, Ventas


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
        raw_data = file.read()

        # Detectar codificacion
        result = chardet.detect(raw_data)
        print(f'resultado de la codificaión del fichero es: {result}')
        encoding = result['encoding']
        print(f'la codificación del fichero es: {encoding}')

        # Leyendo el fichero enviado en el formulario
        cvs_file = raw_data.decode(encoding)
        #cvs_file = raw_data

        # Leyendo cada línea del fichero
        lines = cvs_file.split('\n')

        # Con Pandas
        # file = pd.read_excel('2024-07-15-Convertido_a_libro_excel_97-2003.xls')
        #
        # iterar por una sola columna
        # for i in range(len(file['Departamento'])):
            # print(file['Departamento'][i])
        #
        #
        # Iterar por filas
        # for i in range(len(file)):
            # print(file.iloc[i])
        #
        # Insertar filas en la Base de Datos
        # Insertando los Departamentos
        for line in lines[1:]:
            fields = line.split(',')
            departamento = fields[5].strip()
            # print(f"viene: {departamento}, a ver si existe")

            # Si el Dpto no existe en la tabla Departamento, se agrega
            if not Departamentos.objects.filter(departamento=departamento).exists():
                # print(f"no existe: {departamento}, se agrega")
                obj = Departamentos(
                    # campo1=row['codigo'],
                    departamento=departamento,
                )
                obj.save()

            # Insertando los productos nuevos con su código en la tabla Productos
            producto = fields[1]
            codigo = fields[0]
            if not Productos.objects.filter(codigo=codigo).exists():
                obj = Productos(
                    codigo=codigo,
                    producto=producto
                )
                obj.save()

            # Insertando las ventas del día que se envió en el formulario
            codigo_venta = Productos.objects.get(codigo=codigo)
            cantidad = float(fields[2])
            # patron_coma_digito = [0-9]{1,3}(\,[0-9]{3})
            # venta = float(fields[3].replace('"', '').replace('$', '').replace(',', ''))
            venta = float(fields[3].replace('"', '').replace('$', '').replace(',', ''))
            costo = float(fields[4].replace('$', '').replace(',', ''))
            calculo = (venta - costo) * cantidad
            departamento_venta = Departamentos.objects.get(departamento=departamento)
            fecha = date

            obj_venta = Ventas(
                producto=codigo_venta,
                cantidad=cantidad,
                venta=venta,
                costo=costo,
                calculo=calculo,
                departamento=departamento_venta,
                fecha=fecha
            )
            obj_venta.save()

        return super().form_valid(form)


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
