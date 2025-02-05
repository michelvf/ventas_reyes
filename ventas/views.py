import pandas as pd
import subprocess
import os
import datetime
import pickle
import xlrd, csv
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm, UploadSQLFileForm, ArchivoExcelForm, DepartamentosForm
from .forms import CalculadoraBilletesForm, LacteosForm, DondeSeVendeMasForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.dates import MonthArchiveView, YearArchiveView, WeekArchiveView, DayArchiveView
from .models import Departamentos, Productos, Ventas, fileUpdate, Contador_billete
from .models import Lacteos
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, F
import pytz

# Index Page
class IndexView(TemplateView):
    template_name = 'ventas/index.html'


# Create your views here.
class ExcelUploadView(FormView):
    """
    Vista para subir los ficheros Excel e insertarlos en al Base de Datos
    """
    template_name = 'ventas/upload.html'

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
            # archivo_uri = form.archivo.url
            URI1 = settings.BASE_DIR
            fichero = f'{URI1}{archivo_uri}'
            fecha = request.POST['fecha']
            # print(f'La fecha que llega al POST es: {fecha}')
            # print(f'Lo que llega del POST: {request.POST}')
            # actualizar = form.cleaned_data['actualizar']
            # print(f'actualizar tiene valor: {actualizar}')
            try:
                # FUNCIONA
                df = pd.read_table(fichero, sep='\t', encoding='iso8859_2') 
                # Prueba
                #df = pd.read_table(request.FILES['archivo'], sep='\t', encoding='iso8859_2')  
                # df = pd.read_table(fichero, sep='\t', encoding='iso8859_2')
                
                # Cambio del tipo de 2 columnas a float64
                df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).astype(float)
                excel_file = df
                # tipos_datos = df.dtypes
            except pd.errors.ParserError:
                df = pd.read_excel(fichero) 

                # Cambio del tipo de 2 columnas a float64
                df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).astype(float)
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
                obj = Productos(
                    codigo=codigo,
                    producto=producto,
                    id_departamento=departamento
                )
                # Guardando en la BD
                obj.save()


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
                    'ventas/success.html',
                    { 'fecha': fecha    }
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


class ShowContadorBilletes(ListView):
    """
    Show the Billete Counter
    """
    model = Contador_billete
    # template_name = 'ventas/contar_billetes.html'
    context_object_name = "billetes"


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


class DepartamentoUpdateView(View):
    """
    Update the value of Departement
    """
    def get(self, request): 
        registros = Departamentos.objects.all()
        formularios = [DepartamentosForm(instance=registro, prefix=str(registro.id)) for registro in registros] 
        context = {'formularios': zip(formularios, registros)}
        return render(
            request,
            'ventas/update_departament.html',
            context
        ) 
        #return render(request, "ventas/update_departament.html", {'departamento': departamento} )

    def post(self, request):
        registros = Departamentos.objects.all()
        for registro in registros:
            formulario = DepartamentosForm(request.POST, instance=registro, prefix=str(registro.id))
            if formulario.is_valid():
                formulario.save()
        return redirect('showdepartamentos')


class SalvaResguardoView(View):
    """
    Show the save SQL data
    """
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


class CalculadoraBilletes(View):
    # form_class = CalculadoraBilletesForm
    template_name = 'ventas/contador_billete_form.html'
    
    def get(self, request, *args, **kawars):
        # billetes = Contador_billete.objects.all()
        form = CalculadoraBilletesForm()
        return render(request, 'ventas/contador_billete_form.html', {'form': form})
    
    def post(self, request, *args, **kawars):
        form = CalculadoraBilletesForm(request.POST)
        billetes = request.POST
        # print(f"llegaron del POST: {billetes}")
        
        if form.is_valid():
            form.cleaned_data
            form.save()
            return HttpResponseRedirect('/ventas/mostrar_conteo_billetes/')
        else:
            return render(request, self.template_name, {'form': form})


class EditarCalculadoraBilletes(UpdateView):
    """
    Editar calculadora de billetes
    """
    model = Contador_billete
    # fields = ['total', 'un_peso', 'tres_pesos', 'cinco_pesos', 'diez_pesos', 'veinte_pesos', 'cincuenta_pesos', 'cien_pesos', 'doscientos_pesos', 'quinientos_pesos', 'mil_pesos', 'comentario']
    template_name = 'ventas/contador_billete_form.html'
    success_url = reverse_lazy('mostrar_conteo_billetes')
    form_class = CalculadoraBilletesForm


class VentasAnualesView(YearArchiveView):
    """
    Ventas Anuales
    """
    queryset= Ventas.objects.all()
    date_field= "fecha"
    make_object_list = True
    allow_future = True


class VentasMensualesView(MonthArchiveView):
    """
    Ventas Mensuales
    """
    queryset= Ventas.objects.all()
    date_field= "fecha"
    allow_future = True


class VentasSemanalesView(WeekArchiveView):
    """
    Ventas Semanales
    """
    queryset= Ventas.objects.all()
    date_field= "fecha"
    week_format= "%W"
    allow_future = True


# ¿Qué dia se vende más?
class DiaQueVendeMas(TemplateView):
    template_name = 'ventas/reporte_dia_vende_mas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ahora = timezone.now()
        inicio_mes = ahora.replace(day=1)
        fin_mes = (inicio_mes + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        
        ventas_mensuales = Ventas.objects.filter(
                fecha__gte=inicio_mes,
                fecha__lte=fin_mes,
                id_producto__id_departamento__punto_de_venta=True
            ).values(
                'fecha'
            ).annotate(
                venta_cantidad=Sum('cantidad'),
                venta_total=Sum('calculo')
            )

        print(f"ventas por días: {ventas_mensuales}")
        # Crear un diccionario para almacenar los resultados
        resumen_mensual = {}

        context['resumen_mensual'] = ventas_mensuales
        context['fecha'] =  inicio_mes
            
        return context

# ¿En qué punto de venta se vende más?
class DondeSeVendeMas(View):
    """
    Dónde se vende más por Puntos de Ventas, se escoge la fecha a buscar
    """
    template_name = 'ventas/reporte_mensual_departamento.html'

    def buscar_y_calcular(self, fecha_entrada):
        print(f"en el procesamiento: la fecha que llega es: {fecha_entrada}")
        inicio_mes = fecha_entrada.replace(day=1, month=1)
        fin_mes = (inicio_mes + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        print(f"inicio_mes: {inicio_mes}, fin_mes: {fin_mes}")
        
        # Obtener ventas del mes actual
        ventas_mensuales = Ventas.objects.filter(
            #fecha__gte=inicio_mes,
            #fecha__lte=fin_mes,
            fecha__range=(inicio_mes, fin_mes),
            id_producto__id_departamento__punto_de_venta=True
        )

        # Crear un diccionario para almacenar los resultados
        resumen_mensual = {}

        # Inicializar el diccionario con los días y departamentos
        for i in range((fin_mes - inicio_mes).days + 1):
            dia = inicio_mes + datetime.timedelta(days=i)
            resumen_mensual[dia.strftime('%d')] = {}
            for departamento in Departamentos.objects.filter(punto_de_venta=True):
                resumen_mensual[dia.strftime('%d')][departamento.departamento] = {
                    'cantidad_vendida': 0,
                    'total_vendido': 0,
                    'suma': 0
                }

        # print(resumen_mensual)
        # Rellenar el diccionario con los datos de ventas
        for venta in ventas_mensuales:
            dia = venta.fecha.strftime('%d')
            departamento = venta.id_producto.id_departamento.departamento
            resumen_mensual[dia][departamento]['cantidad_vendida'] += venta.cantidad
            resumen_mensual[dia][departamento]['total_vendido'] += venta.calculo
            #resumen_mensual[dia][departamento]['suma'] += resumen_mensual[dia][departamento]['total_vendido']

        return resumen_mensual
        
    
    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)
        ahora = timezone.now()
        context = {}
        context['fecha'] =  ahora
        context['resumen_mensual'] = self.buscar_y_calcular(ahora)
        
        return render(request, 'ventas/reporte_mensual_departamento.html', context)
    
    
    def post(self, request):
        print('dentro del post, voy a capturar el formulario')
        form = DondeSeVendeMasForm(request.POST)
        print(f"dentro del post, a ver si el formulario es válido")
        if form.is_valid():
        # if request.method == "POST":
            # context = super().get_context_data(**kwargs)
            # form.cleaned_data
            #print("request: ", request.POST)
            print(f"formulario válido, a procesar entonces")
            # anno = request.POST.get('anno')
            # mes = request.POST.get('mes')
            anno = form.cleaned_data['anno']
            mes = form.cleaned_data['mes']
            print(f"Dentro del POST: MES: {mes}, AÑO: {anno}")
            zona_horaria = pytz.timezone('America/Havana')
            fecha = datetime.datetime(year=anno, month=mes,day=1, tzinfo=zona_horaria)
            # fecha = datetime.datetime(year=anno, month=mes,day=1)
            print(f"fecha a enviar para procesamiento: {fecha}")
            context = {}
            context['fecha'] =  fecha
            context['resumen_mensual'] = self.buscar_y_calcular(fecha)
            
            #print(f"voy a renderizar, el contexto es: {context}")
        
        return render(request, 'ventas/reporte_mensual_departamento.html', context)


class LacteosListView(ListView):
    """
    Listar los lácteos
    """
    model = Lacteos
    template_name = 'ventas/lacteos_listview.html' 


class LacteosCreate(CreateView):
    """
    Crear nuevos acteos
    """
    model = Lacteos
    form_class = LacteosForm
    template_name = 'ventas/lacteos_form.html'
    success_url= "/ventas/listado_lacteos/"
    success_message= "%(name)s was created successfully"


class LacteosUpdate(UpdateView):
    """
    Crear nuevos acteos
    """
    model = Lacteos
    form_class = LacteosForm
    template_name = 'ventas/lacteos_form.html'
    success_url= "/ventas/listado_lacteos/"
    success_message= "%(name)s was created successfully"
    
    
# ventas de lácteos, por departamentos
# ventas por departamentos
# dpto Don Reyes, no sale el helado 0250 lts


"""
Punto la Parada:
21.73781, -82.75416

Punto Di MUU
21.74459, -82.75517
"""