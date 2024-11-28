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
        date = form.cleaned_data['datefilter']
        file = form.cleaned_data['file']
        raw_data = file.read()

        # Detectar codificacion
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        cvs_file = raw_data.decode(encoding)

        lines = cvs_file.split('\n')

        # Insertar filas en la Base de Datos
        # for _, row in df.iterrows():
        for line in lines[1:]:
            fields = line.split(';')
            departamento = fields[5].strip()
            # print(f"viene: {departamento}, a ver si existe")
            if not Departamentos.objects.filter(departamento=departamento).exists():
                # print(f"no existe: {departamento}, se agrega")
                obj = Departamentos(
                    # campo1=row['codigo'],
                    departamento=departamento,
                )
                obj.save()

            producto = fields[1]
            codigo = fields[0]
            if not Productos.objects.filter(codigo=codigo).exists():
                obj = Productos(
                    codigo=codigo,
                    producto=producto
                )
                obj.save()

            codigo_venta = Productos.objects.get(codigo=codigo)
            cantidad = float(fields[2])
            venta = float(fields[3].replace('$', '').replace(',', ''))
            costo = float(fields[4].replace('$', '').replace(',', ''))
            calculo = (venta - costo) * cantidad
            departamento_venta = Departamentos.objects.get(departamento=departamento)
            fecha = datetime.datetime.now()

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
