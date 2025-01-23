import pandas as pd
import subprocess
import os
import datetime
import pickle
import xlrd, csv
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm, UploadSQLFileForm, ArchivoExcelForm
from django.views.generic.edit import FormView
from rest_framework.views import APIView
from django.views.generic import TemplateView
from .models import Departamentos, Productos, Ventas, fileUpdate
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.conf import settings


# Index Page
class IndexView(TemplateView):
    template_name = 'ventas/index.html'


# Create your views here.
class ExcelUploadView(FormView):
    """
    Vista para subir los ficheros Excel e insertarlos en al Base de Datos
    """
    template_name = 'ventas/upload.html'
    # template_name = 'ventas/subir.html'
    # form_class = ExcelUploadForm
    # success_url = '/ventas/success/'
    # success_url = reverse_lazy('success')

    # Si recibo un get, se manda la plantilla con el formulario en blanco
    def get(self, request):
        #form = self.form_class()
        form = ArchivoExcelForm()
        return render(request, self.template_name, {'form': form})

    # Si se recibe el método POST, se hace el proceso de cargar los datos
    def post(self, request):
        # Intento 12-01-25
        form = ArchivoExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_model = form.save()
            archivo_uri = archivo_model.archivo.url
            URI1 = settings.BASE_DIR
            fichero = f'{URI1}{archivo_uri}'
            fecha = request.POST['fecha']
            # print(f'La fecha que llega al POST es: {fecha}')
            print(f'Lo que llega del POST: {request.POST}')
            # actualizar = form.cleaned_data['actualizar']
            # print(f'actualizar tiene valor: {actualizar}')
            try:
                # FUNCIONA
                df = pd.read_table(fichero, sep='\t', encoding='iso8859_2') 
                # Prueba
                #df = pd.read_table(request.FILES['archivo'], sep='\t', encoding='iso8859_2')  
                # df = pd.read_table(fichero, sep='\t', encoding='iso8859_2')
                
                # Cambio del tipo de 2 columnas a float64
                df['Precio Usado'] = df['Precio Usado'].replace({'\$': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({'\$': ''}, regex=True).astype(float)
                excel_file = df
                # tipos_datos = df.dtypes
            except pd.errors.ParserError:
                df = pd.read_excel(fichero) 

                # Cambio del tipo de 2 columnas a float64
                df['Precio Usado'] = df['Precio Usado'].replace({'\$': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({'\$': ''}, regex=True).astype(float)
                excel_file = df
            except Exception as e:
                error_message = f"Error al leer el fichero: {e}"
                # form.
                return render(request, self.template_name, {'form': form, 'error': error_message})
        
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

                Productos.objects.update_or_create(
                    codigo=codigo,
                    producto=producto,
                    id_departamento=departamento
                )
                #obj = Productos(
                #    codigo=codigo,
                #    producto=producto,
                #    id_departamento=departamento
                #)
                # Guardando en la BD
                # obj.save()

        # Borrar los que se van a actualizar
        # if actualizar:
        #     ventas = Ventas.objects.filter(fecha=fecha).delete()
            # print(f"se van a borrar: {ventas}")
        # else:
        #     fileUp = fileUpdate(fecha=fecha)
        #     fileUp.save()

        # Insertando las Ventas
        for i in range(len(excel_file)):
            # Leyendo una fila
            fila = excel_file.iloc[i]
            
            # Buscando el id del producto a insertar
            codigo_venta = Productos.objects.get(codigo=fila['Codigo'])
            # Tomando valores del Excel
            # cantidad = float(fila['Cantidad'])
            # venta = float(fila['Precio Usado'].apply(lambda x: x.replace('$', '')))
            # costo = float(fila['Precio Costo'].apply(lambda x: x.replace('$', '')))
            cantidad = fila['Cantidad']
            venta = fila['Precio Usado']
            costo = fila['Precio Costo']
            calculo = (venta - costo) * cantidad
            # Buscando el valor del id del Departamento de la venta
            # departamento_venta = Departamentos.objects.get(departamento=fila['Departamento'])
            # Tomando la fecha que se insertó
            # fecha = date

            # Preparado para insertarlo en el modelo Departamento
            Ventas.objects.update_or_create(
                id_producto=codigo_venta,
                cantidad=cantidad,
                venta=venta,
                costo=costo,
                calculo=calculo,
                fecha=fecha
            )
            # obj_venta = Ventas(
            #     id_producto=codigo_venta,
            #     cantidad=cantidad,
            #     venta=venta,
            #     costo=costo,
            #     calculo=calculo,
            #     # departamento=departamento_venta,
            #     fecha=fecha
            # )
            # # Guardando en la BD
            # # print(f"Se va a guardar: {obj_venta}")
            # obj_venta.save()
        
        # return render(request, self.template_name, {'form': form})
        return render(
                    request,
                    'ventas/success.html'
                )
        # Recibir el formulario
        # form = self.form_class(request.POST, request.FILES)
        # si es válido, comienza proceso
        #if form.is_valid():
            # recibir todas las variables enviadas
        #    excel_file = request.FILES['file']
        #    date = request.POST['datefilter']
        #    actualizar = request.POST['actualizar']
            
            # f = xlrd.open_workbook(excel_file).sheet_by_index(0)
            # formar la URI del fichero a guardar
        #    nombre = f'subiendo_datos.xls'
        #    lugar = settings.MEDIA_ROOT
        #    fichero = f'{lugar}/{nombre}'
            
            # guardando el fichero
        #    with open(fichero, 'wb') as f:
        #        pickle.dump(excel_file, f)
        #    f.close()
            
            # Preprando para modificar el fichero
            # cambio = f'{lugar}/cambio.csv'
            # q = open(fichero, 'r')
            # r = open(cambio, 'w')
            # i = 0
            
            # leyendo el fichero para modificarlo
            # for line in q.readlines():
            #     if i != 0:
            #         r.write(line)
            #     i += 1
            # r.close()
            
            # intento de leer el fichero
        #    try:
                # df = pd.read_csv(fichero)
        #        df = xlrd.open_workbook(fichero).sheet_by_index(0)
                # Aquí puedes realizar más validaciones o procedimientos con el DataFrame
        #        return HttpResponse("Archivo leído correctamante")
        #    except Exception as e:
        #        error_message = f"Error al leer el fichero: {e}"
        #        form.add_error('file', 'Error al leer el fichero: {}'.format(e))
                # return render(request, self.template_name, {'form': form, 'error': error_message})
        #        return self.form_invalid(form)
        #return render(request, self.template_name, {'form': form})


    # def form_valid(self, form):
    #     """
    #     Obtener el fichero y fecha, y registrar sus datos en la Base de Datos
    #     """
    #     # Obteniendo los valores del formulario
    #     date = form.cleaned_data['datefilter']
    #     file = form.cleaned_data['file']
        
    #     actualizar = form.cleaned_data['actualizar']
    #     print(f"Llegó del forumario: date: {date}, file: {file}, actualizar: {actualizar}")

    #     try:
    #         # Leer el fichero recibido
    #         # raw_data = file.read()

    #         # Con Pandas leer el fichero exel
    #         # excel_file = pd.read_excel(file)
    #         # excel_file = pd.read_table(file, sep="\t", encoding="ISO-8859-1")
    #         # excel_file = pd.read_excel(file, encoding='utf-8')
    #         # excel_file = pd.read_table(file, sep="\t", encoding='ISO-8859-1')
    #         # wb = xlrd.open_workbook(file, encoding_override='CORRECT_ENCODING')
    #         #excel_file = pd.read_excel(file, engine='xlrd')
    #         excel_file = pd.read_table(file, sep='\t', encoding='iso8859_15')
            
    #         # excel_file = excel_file.replace('\t', ' ', regex=True) 
            
    #         excel_file['Precio Usado'] = excel_file['Precio Usado'].replace({'\$': ''}, regex=True).astype(float)
    #         excel_file['Precio Costo'] = excel_file['Precio Costo'].replace({'\$': ''}, regex=True).astype(float)
    #           excel_file['Precio Costo'].replace({'\$': ''}, regex=True).replace('$', '').astype(float)
    #            
    #     except Exception as e:
    #         # form.add_error('file', 'Error al leer el fichero, debe convertirlo a fichero de excel como indica la figura: {}'.format(e))
    #         form.add_error('file', 'Error al leer el fichero: {}'.format(e))
    #         return self.form_invalid(form)
        
    

    #     # return JsonResponse({'mensaje': 'Datos recibidos correctamente!'})
    #     messages.success(self.request, 'Fichero subido y leído correctamente')
    #     return super().form_valid(form)


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


class SalvaResguardoView(View):
    
    template_name = 'ventas/salvar_restaurar.html'
    

class BackupRestoreSQLiteView(View):
    template_name = 'ventas/backup_restore.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'backup' in request.POST:
            return self.backup_database()
        elif 'restore' in request.POST and request.FILES['sql_file']:
            return self.restore_database(request.FILES['sql_file'])
        return redirect('backup_restore')

    def backup_database(self):
        # Ruta al archivo de base de datos
        db_path = settings.DATABASES['default']['NAME']
        # Comando para hacer el backup de la base de datos
        aplicacion = settings.ROOT_URLCONF.split('.')[0]
        fecha = datetime.datetime.now().strftime('%d-%m-%Y_%H_%M_%S')
        nombre = f'salva_BaseDeDatos-{aplicacion}-{fecha}.sql'
        lugar = settings.MEDIA_ROOT
        fichero = f'{lugar}/{nombre}'
        command = f"sqlite3 {db_path} .dump > {fichero}"
        subprocess.run(command, shell=True)
        with open(fichero, "rb") as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response

    def restore_database(self, sql_file):
        fs = FileSystemStorage()
        filename = fs.save(sql_file.name, sql_file)
        file_path = fs.path(filename)

        # Ruta al archivo de base de datos
        db_path = settings.DATABASES['default']['NAME']
        # Comando para restaurar la base de datos
        command = f"sqlite3 {db_path} < {file_path}"
        subprocess.run(command, shell=True)
        return redirect('backup_restore')


class BackupRestorePGSQLView(View):
    template_name = 'ventas/backup_restore.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        if 'backup' in request.POST:
            return self.backup_database()
        elif 'restore' in request.POST and request.FILES['sql_file']:
            return self.restore_database(request.FILES['sql_file'])
        return redirect('backup_restore')
    
    def backup_database(self):
        # Comando para hacer el backup de la base de datos
        aplicacion = settings.ROOT_URLCONF.split('.')[0]
        fecha = datetime.datetime.now().strftime('%d-%m-%Y_%H_%M_%S')
        nombre = f'salva_BaseDeDatos-{aplicacion}-{fecha}.sql'
        lugar = settings.MEDIA_ROOT
        fichero = f'{lugar}/{nombre}'
        command = f"pg_dump -U {settings.DATABASES['default']['USER']} -h {settings.DATABASES['default']['HOST']} -p {settings.DATABASES['default']['PORT']} {settings.DATABASES['default']['NAME']} > {fichero}"
        subprocess.run(command, shell=True)
        with open("backup.sql", "rb") as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    
    def restore_database(self, sql_file):
        fs = FileSystemStorage()
        filename = fs.save(sql_file.name, sql_file)
        file_path = fs.path(filename)
        # Comando para restaurar la base de datos
        command = f"psql -U {settings.DATABASES['default']['USER']} -h {settings.DATABASES['default']['HOST']} -p {settings.DATABASES['default']['PORT']} {settings.DATABASES['default']['NAME']} < {file_path}"
        subprocess.run(command, shell=True)
        
        return redirect('backup_restore')


class CalculadoraBilletes(TemplateView):
    template_name = 'ventas/calculadora_billetes.html'

"""
Punto la Parada:
21.73781, -82.75416

Punto Di MUU
21.74459, -82.75517
"""