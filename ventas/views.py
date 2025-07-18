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
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.dates import MonthArchiveView, YearArchiveView, WeekArchiveView, DayArchiveView
from .models import Departamentos, Productos, Ventas, fileUpdate, Contador_billete
from .models import Lacteos, Cuenta, Tipo_cuenta, Cuenta_historico
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, F
from django.core.paginator import Paginator
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
                # df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).astype(float)
                # df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).astype(float)

                # Para Eleventa 2025
                df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).replace({r',': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).replace({r',': ''}, regex=True).astype(float)
                excel_file = df
                # tipos_datos = df.dtypes
            except pd.errors.ParserError:
                df = pd.read_excel(fichero) 

                # Cambio del tipo de 2 columnas a float64
                # df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).astype(float)
                # df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).astype(float)
                df['Precio Usado'] = df['Precio Usado'].replace({r'\$': ''}, regex=True).replace({r',': ''}, regex=True).astype(float)
                df['Precio Costo'] = df['Precio Costo'].replace({r'\$': ''}, regex=True).replace({r',': ''}, regex=True).astype(float)
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
        for i in range(len(excel_file['Descripción'])):

            # Tomando el valor de un departamento
            producto = excel_file['Descripción'][i]
            codigo = excel_file['Código'][i]
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

        # Insertando las Ventas
        for i in range(len(excel_file)):
            # Leyendo una fila
            fila = excel_file.iloc[i]

            # Buscando el id del producto a insertar
            codigo_venta = Productos.objects.get(codigo=fila['Código'])
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
    # paginate_by = 20


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
        # billetes = request.POST
        # print(f"llegaron del POST: {billetes}")

        if form.is_valid():
            
            # Validar los datos llegados del formulario
            form.cleaned_data
            #form('sub_total') = form.total + sub_total.sub_total
            
            saldo = Cuenta.objects.get(cuenta="Efectivo")
            registro = form.cleaned_data['total']

            # tipo = form.cleaned_data['tipo_cuenta']
            tipo = int(request.POST.get('tipo_cuenta'))
            
            if tipo == 1:
                form.instance.sub_total = saldo.saldo + registro
            else:
                form.instance.sub_total = saldo.saldo - registro
            
            # Guardar los datos del formulario
            form.save()
            
            # tipo = request.POST.get('tipo_cuenta')
            un = int(request.POST.get('un_peso'))
            tres = int(request.POST.get('tres_pesos'))
            cinco = int(request.POST.get('cinco_pesos'))
            diez = int(request.POST.get('diez_pesos'))
            veinte = int(request.POST.get('veinte_pesos'))
            cincuenta = int(request.POST.get('cincuenta_pesos'))
            cien = int(request.POST.get('cien_pesos'))
            doscientos = int(request.POST.get('doscientos_pesos'))
            quinientos = int(request.POST.get('quinientos_pesos'))
            mil = int(request.POST.get('mil_pesos'))
            
            if tipo == 1:
                # print(f"Es de tipo {type(tipo)}, es un Crédito se suman: {registro}")
                saldo.saldo += int(registro)
                # saldo.sub_cuenta += form.total
                saldo.un_peso += un if un is not None else 0
                saldo.tres_pesos += tres if tres is not None else 0
                saldo.cinco_pesos += cinco if cinco is not None else 0
                saldo.diez_pesos += diez if diez is not None else 0
                saldo.veinte_pesos += veinte if veinte is not None else 0
                saldo.cincuenta_pesos += cincuenta if cincuenta is not None else 0
                saldo.cien_pesos += cien if cien is not None else 0
                saldo.doscientos_pesos += doscientos if doscientos is not None else 0
                saldo.quinientos_pesos += quinientos if quinientos is not None else 0
                saldo.mil_pesos += mil if mil is not None else 0
            else:
                # print(f"Es de tipo {type(tipo)}, es un Débito se resta: {registro}")
                saldo.saldo -= int(registro)
                # saldo.sub_cuenta -= form.total
                saldo.un_peso -= un if un is not None else 0
                saldo.tres_pesos -= tres if tres is not None else 0
                saldo.cinco_pesos -= cinco if cinco is not None else 0
                saldo.diez_pesos -= diez if diez is not None else 0
                saldo.veinte_pesos -= veinte if veinte is not None else 0
                saldo.cincuenta_pesos -= cincuenta if cincuenta is not None else 0
                saldo.cien_pesos -= cien if cien is not None else 0
                saldo.doscientos_pesos -= doscientos if doscientos is not None else 0
                saldo.quinientos_pesos -= quinientos if quinientos is not None else 0
                saldo.mil_pesos -= mil if mil is not None else 0
            
            # print(f"Saldo actualizado: {saldo.saldo}")
            # Guardar los datos actualizados en la Cuenta
            saldo.save()

            return HttpResponseRedirect('/ventas/mostrar_conteo_billetes/')
        else:
            return render(request, self.template_name, {'form': form})


class CalculadoraBilletes2(TemplateView):
    """Calculadorade Billetes List View 2"""
    template_name = 'ventas/contador_billete_list2.html'


class EditarCalculadoraBilletes(UpdateView):
    """
    Editar calculadora de billetes
    """
    model = Contador_billete
    template_name = 'ventas/contador_billete_form.html'
    success_url = reverse_lazy('mostrar_conteo_billetes')
    form_class = CalculadoraBilletesForm

    def form_valid(self, form):
        """
        Override form_valid to update Cuenta model when there are changes
        """
        # Get the current instance
        instance = self.get_object()
        
        # Get the current Cuenta
        cuenta = Cuenta.objects.get(cuenta="Efectivo")
        
        # Get the cleaned data from the form
        cleaned_data = form.cleaned_data
        
        # Get the current values from the database
        current_values = {
            'un_peso': instance.un_peso,
            'tres_pesos': instance.tres_pesos,
            'cinco_pesos': instance.cinco_pesos,
            'diez_pesos': instance.diez_pesos,
            'veinte_pesos': instance.veinte_pesos,
            'cincuenta_pesos': instance.cincuenta_pesos,
            'cien_pesos': instance.cien_pesos,
            'doscientos_pesos': instance.doscientos_pesos,
            'quinientos_pesos': instance.quinientos_pesos,
            'mil_pesos': instance.mil_pesos
        }
        
        # Get the new values from the form
        new_values = {
            'un_peso': cleaned_data.get('un_peso', 0),
            'tres_pesos': cleaned_data.get('tres_pesos', 0),
            'cinco_pesos': cleaned_data.get('cinco_pesos', 0),
            'diez_pesos': cleaned_data.get('diez_pesos', 0),
            'veinte_pesos': cleaned_data.get('veinte_pesos', 0),
            'cincuenta_pesos': cleaned_data.get('cincuenta_pesos', 0),
            'cien_pesos': cleaned_data.get('cien_pesos', 0),
            'doscientos_pesos': cleaned_data.get('doscientos_pesos', 0),
            'quinientos_pesos': cleaned_data.get('quinientos_pesos', 0),
            'mil_pesos': cleaned_data.get('mil_pesos', 0)
        }
        
        # Calculate differences and update Cuenta
        for denomination, new_value in new_values.items():
            current_value = current_values[denomination]
            difference = new_value - current_value
            
            if difference != 0:  # Only update if there's a change
                if denomination == 'un_peso':
                    cuenta.un_peso += difference
                elif denomination == 'tres_pesos':
                    cuenta.tres_pesos += difference
                elif denomination == 'cinco_pesos':
                    cuenta.cinco_pesos += difference
                elif denomination == 'diez_pesos':
                    cuenta.diez_pesos += difference
                elif denomination == 'veinte_pesos':
                    cuenta.veinte_pesos += difference
                elif denomination == 'cincuenta_pesos':
                    cuenta.cincuenta_pesos += difference
                elif denomination == 'cien_pesos':
                    cuenta.cien_pesos += difference
                elif denomination == 'doscientos_pesos':
                    cuenta.doscientos_pesos += difference
                elif denomination == 'quinientos_pesos':
                    cuenta.quinientos_pesos += difference
                elif denomination == 'mil_pesos':
                    cuenta.mil_pesos += difference
        
        # Update saldo based on changes
        cuenta.saldo = (
            cuenta.un_peso * 1 +
            cuenta.tres_pesos * 3 +
            cuenta.cinco_pesos * 5 +
            cuenta.diez_pesos * 10 +
            cuenta.veinte_pesos * 20 +
            cuenta.cincuenta_pesos * 50 +
            cuenta.cien_pesos * 100 +
            cuenta.doscientos_pesos * 200 +
            cuenta.quinientos_pesos * 500 +
            cuenta.mil_pesos * 1000
        )
        
        # Save the Cuenta instance
        cuenta.save()
        
        # Call the parent form_valid method to save the Contador_billete instance
        return super().form_valid(form)


class BorrarCalculadoraBilletes(DeleteView):
    """
    Borrar un registro y devolver el dinero al total
    """
    model = Contador_billete
    success_url = reverse_lazy("mostrar_conteo_billetes")

    def post(self, request, *args, **kwargs):
        # Obtener el objeto antes de eliminarlo
        self.object = self.get_object()

        # Realizar alguna acción antes de eliminar el objeto
        # Por ejemplo, registrar el borrado en un log
        efectivo = Cuenta.objects.get(cuenta="Efectivo")
        tipo_cuenta = str(self.object.tipo_cuenta)

        if tipo_cuenta == 'Entrada':
            # print("Es un Crédito, lo voy a retar")
            efectivo.un_peso -= self.object.un_peso
            efectivo.tres_pesos -= self.object.tres_pesos
            efectivo.cinco_pesos -= self.object.cinco_pesos
            efectivo.diez_pesos -= self.object.diez_pesos
            efectivo.veinte_pesos -= self.object.veinte_pesos
            efectivo.cincuenta_pesos -= self.object.cincuenta_pesos
            efectivo.cien_pesos -= self.object.cien_pesos
            efectivo.doscientos_pesos -= self.object.doscientos_pesos
            efectivo.quinientos_pesos -= self.object.quinientos_pesos
            efectivo.mil_pesos -= self.object.mil_pesos
            efectivo.saldo -= self.object.total
        else:
            # print("Es un Débito, lo voy a sumar")
            efectivo.un_peso += self.object.un_peso
            efectivo.tres_pesos += self.object.tres_pesos
            efectivo.cinco_pesos += self.object.cinco_pesos
            efectivo.diez_pesos += self.object.diez_pesos
            efectivo.veinte_pesos += self.object.veinte_pesos
            efectivo.cincuenta_pesos += self.object.cincuenta_pesos
            efectivo.cien_pesos += self.object.cien_pesos
            efectivo.doscientos_pesos += self.object.doscientos_pesos
            efectivo.quinientos_pesos += self.object.quinientos_pesos
            efectivo.saldo += self.object.total
        
        efectivo.save()
    
        # print(f"Registro eliminado id: {self.object.id}")
        # print(f"Registro eliminado tipo_cuenta: º{tipo_cuenta}º")
        # comprobar = str(tipo_cuenta) == 'Entrada'
        # print(f"Comprobación si es Entrada: {comprobar}")

        # También podrías ejecutar acciones como enviar un correo o modificar otra tabla

        # Llamar al método `delete()` original
        response = super().post(request, *args, **kwargs)

        # Si quieres cambiar la redirección, puedes hacerlo aquí
        return response


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

        inicio_mes = fecha_entrada.replace(day=1, hour=1, minute=0, second=0)
        fin_mes = (inicio_mes + datetime.timedelta(days=32)).replace(day=1, hour=23, minute=59, second=59) - datetime.timedelta(days=1)
        # print(f"inicio_mes: {inicio_mes}, fin_mes: {fin_mes}")
        #        inicio_mes = fecha_entrada.replace(day=1, hour=0, minute=0, second=0)
        #        fin_mes = (inicio_mes + datetime.timedelta(days=32)).replace(day=1,hour=23,minute=59,second=59) - datetime.timedelta(days=1)
        #        print(f"inicio_mes: {inicio_mes}, fin_mes: {fin_mes}")
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
                    # 'suma': 0
                }

        # print(resumen_mensual)
        # Rellenar el diccionario con los datos de ventas
        for venta in ventas_mensuales:
            dia = venta.fecha.strftime('%d')
            departamento = venta.id_producto.id_departamento.departamento
            print(f"Venta cantidad: {venta.cantidad}")
            resumen_mensual[dia][departamento]['cantidad_vendida'] += venta.cantidad
            resumen_mensual[dia][departamento]['total_vendido'] += venta.calculo
            #resumen_mensual[dia][departamento]['suma'] += resumen_mensual[dia][departamento]['total_vendido']

        return resumen_mensual


    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)
        ahora = timezone.now()
        context = {}
        context['fecha'] = ahora
        context['resumen_mensual'] = self.buscar_y_calcular(ahora)

        return render(request, 'ventas/reporte_mensual_departamento.html', context)


    def post(self, request):
        #print('dentro del post, voy a capturar el formulario')
        form = DondeSeVendeMasForm(request.POST)
        #print(f"dentro del post, a ver si el formulario es válido")
        if form.is_valid():
        # if request.method == "POST":
            # context = super().get_context_data(**kwargs)
            # form.cleaned_data
            #print("request: ", request.POST)
            #print(f"formulario válido, a procesar entonces")
            # anno = request.POST.get('anno')
            # mes = request.POST.get('mes')
            anno = form.cleaned_data['anno']
            mes = form.cleaned_data['mes']

            #print(f"Dentro del POST: MES: {mes}, AÑO: {anno}")
            # zona_horaria = pytz.timezone('America/Havana')
            zona_horaria = pytz.timezone('UTC')
            fecha = datetime.datetime(year=anno, month=mes,day=1,tzinfo=zona_horaria)

            print(f"Dentro del POST: MES: {mes}, AÑO: {anno}")
        #     fecha1 = timezone.now()
        #     fecha = fecha1.replace(year=anno, month=mes,day=1,hour=5,minute=0,second=0)
            # fecha = datetime.datetime(year=anno, month=mes,day=1)
            #print(f"fecha a enviar para procesamiento: {fecha}")
            context = {}
            context['fecha'] = fecha
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


class CalculoPorcientoPrecio(TemplateView):
    template_name = 'ventas/calculo_porciento.html'


class PruebaView(TemplateView):
    """Para Pruebas"""
    template_name = 'ventas/probar.html'



"""
Punto la Parada:
21.73781, -82.75416

Punto Di MUU
21.74459, -82.75517
"""
