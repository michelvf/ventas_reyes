import datetime
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework import authentication
from ventas.models import Departamentos, Productos, Ventas, fileUpdate, Lacteos, Cuenta, Contador_billete
from .serializers import DepartamentoSerializer, ProductosSerializer
from .serializers import VentaSerializer, VentasPorFechasSerializer, AnnosDeVentaSerializer
from .serializers import VentasPorFechasTodoSerializer, ProdxDepSerializer
from .serializers import ProdMasVendidosSerializer, SumarVentasPorFechasSerializer
from .serializers import ProdMasVendidosVarSerializer, LacteosSerializer, AnnoSerializer
from .serializers import FicherosSubidosSerializer, VentaSemanalSerializer, CuentaBilletesSerializer
from .serializers import NominaDepartamentoSerializer, DiaQueMasVendeSerializar, ContadorBilleteListSerializer
from compras.models import Almacen, Producto, PrecioProducto, Compra, UnidadMedida
from .serializers import AlmacenSerializer, ProductoSerializer, CompraSerializer
from .serializers import PrecioProductoSerializer, NominaCargoSerializer, MesesSerializer
from .serializers import CategoriaSerializer, ProduccionProductoSerializer, ProduccionSerializer, SalidaSerializer
from produccion.models import Categoria, Producto, Produccion, Salida
from nomina.models import DepartamentoNom, Trabajador, Nomina, Cargo
from .serializers import AnnosMesVentasSerializer, DondeSeVendeMasSerializar, SaldoEfectivoSerializer
from django.db.models import Sum, Count, Q, DateField
from django.db.models.functions import TruncDate, Substr
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import ExtractYear, TruncMonth
from django.shortcuts import get_object_or_404
import pytz


# Create your views here.
class ProductosApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer


class DepartamentoApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Departament
    """
    queryset = Departamentos.objects.all()
    serializer_class = DepartamentoSerializer


class FicherosSubidosApiView(viewsets.ReadOnlyModelViewSet):
    """
    Date of the files Up
    """
    queryset = fileUpdate.objects.all()
    serializer_class = FicherosSubidosSerializer


class VentaApiView(viewsets.ReadOnlyModelViewSet):
    """
    API to show the Sellings
    """
    queryset = Ventas.objects.all()
    serializer_class = VentaSerializer


class VentasPorFechas(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = VentasPorFechasSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            # departamento = serializer.validated_data['departamento']
            ventas_fecha = Ventas.objects.filter(fecha__range=[start_date, end_date])
            serializer_other = VentasPorFechasTodoSerializer(ventas_fecha, many=True)
            # return Response(ventas_fecha.values(), status=status.HTTP_200_OK)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SumaPorFechasAPI(APIView):
    """
    Api to show the sum of seld for dates
    """

    def get(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Por favor, proporcione las fechas de inicio y fin"}, status=400)

        sumatoria = Ventas.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).annotate(
            fechas=TruncDate('fecha')
        ).values('fecha').annotate(
            suma=Sum('calculo')
        ).order_by('fecha')

        return Response(sumatoria)


class ProductXDeptoListView(APIView):
    """
    Api to show the cant of Product for Departament
    """
    # queryset = Departamentos.objects.annotate(num_prod=Count('producto'))
    # serializer = ProductXDepto()

    def get(self, request):
        departamentos = Departamentos.objects.annotate(num_prod=Count('productos'))
        serializer = ProdxDepSerializer(departamentos, many=True)

        return Response(serializer.data)


class ProductMasVendidoAPI(APIView):
    """
    API to show the products more sales
    """
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = ProdMasVendidosVarSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            departamento = serializer.validated_data['departamento']
            produ_mas_vendido = (Productos.objects
                .filter(
                    productos__fecha__range=[start_date, end_date],
                    id_departamento__in=departamento
                )
                .annotate(
                    total_vendido=Sum('productos__cantidad'),
                    total_ventas=Sum('productos__calculo')
                )
                .order_by('-total_vendido')[:10]
            )
            serializer_other = ProdMasVendidosSerializer(produ_mas_vendido, many=True)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LacteosAPI(APIView):
    """
    API to show the best selling dairy products
    """
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = ProdMasVendidosVarSerializer(data=request.data)
        # lacteos = ['YOGUR','HELA','REQ','SUER','ENERG','PALE', 'QUE']
        lacteos = Lacteos.objects.all().values('nombre')
        condiciones = Q()
        for palabra in lacteos:
            condiciones |= Q(id_producto__producto__istartswith=palabra['nombre'])
            # condiciones |= Q(id_producto__producto__startswith=palabra)
            # condiciones |= Q(id_producto__producto__icontains=palabra)
            # condiciones |= Q(id_producto__producto__contains=palabra)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            departamento = serializer.validated_data['departamento']
            lacteos_vendidos = Ventas.objects.filter(condiciones).annotate(
                producto_s=Substr('id_producto__producto', 1, 20),
            ).filter(
                # id_producto__id_departamento__punto_de_venta=departamento,
                id_producto__id_departamento__in=departamento,
                fecha__range=[start_date, end_date],
            ).values(
                'producto_s'
            ).annotate(
                total_vendido=Sum('cantidad'),
                total_ventas=Sum('calculo'),
            #    codigo='id_producto__codigo',
            # ).order_by('total_vendido')
            ).order_by('producto_s')

            serializer_other = LacteosSerializer(lacteos_vendidos, many=True)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LacteosSemanaAPI(APIView):
    """
    API to show the best selling weekly products
    """
    def get(self, request):
        # lacteos = ['YOGUR','HELA','REQ','SUER','ENERG','PALE', 'QUESO']
        lacteos = Lacteos.objects.all().values('nombre')
        condiciones = Q()
        departamento_punto_venta = True
        # Buscando la ultima fecha
        tamano = len(fileUpdate.objects.all())
        ultimo = fileUpdate.objects.all()[tamano - 1]
        to_day = ultimo.fecha
        a_week = ultimo.fecha  + timedelta(days=-7)
        #to_day = datetime.now()
        #a_week = datetime.now() + timedelta(days=-7)

        for palabra in lacteos:
            condiciones |= Q(id_producto__producto__istartswith=palabra['nombre'])
        lacteos_vendidos = Ventas.objects.filter(condiciones).annotate(
            producto_s=Substr('id_producto__producto', 1, 20),
        ).filter(
            id_producto__id_departamento__punto_de_venta=departamento_punto_venta,
            fecha__range=[a_week, to_day],
        ).values(
            'producto_s'
        ).annotate(
            total_vendido=Sum('cantidad'),
            total_ventas=Sum('calculo'),
        ).order_by('-total_vendido')
        #).order_by('-cantidad')

        serializer_other = LacteosSerializer(lacteos_vendidos, many=True)
        return Response(serializer_other.data, status=status.HTTP_200_OK)


class VentaSemanalAPI(APIView):
    """
    Ventas en la semana
    """
    def get(self, request):

        week_sales = Ventas.objects.annotate(
                fecha_agregada=TruncDate('fecha', output_field=DateField())
            ).values(
                'fecha_agregada'
            ).annotate(
                total_vendido=Sum('calculo')
            ).order_by('-fecha_agregada')[:7]

        # El bueno antes de cambiar
        # week_sales = Ventas.objects.filter(
        #         fecha__gte=a_week
        #     ).annotate(
        #         fecha_agregada=TruncDate('fecha', output_field=DateField())
        #     ).values(
        #         'fecha_agregada'
        #     ).annotate(
        #         total_vendido=Sum('calculo')
        #     ).order_by('fecha_agregada')
            
        serializer = VentaSemanalSerializer(week_sales, many=True)
        
        return Response(serializer.data)



############### Compra ##############

# Create your views here.
class AlmacenApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer


# Create your views here.
class ProductoApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# Create your views here.
class PrecioProductoApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = PrecioProducto.objects.all()
    serializer_class = PrecioProductoSerializer


# Create your views here.
class CompraApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer


class UltimoPrecio(APIView):
    """
    Úlitmo percio según el producto
    """
    authentication_classes = [authentication.TokenAuthentication]
    
    def post(self, request):
        prod = request.data['producto']
        # print(f"lo que llega del formulario, del select: {prod}")
        rep = (Compra.objects.filter(producto__id=prod)
            .values('precio_compra')
            .order_by('-fecha')[:1])

        # rep = 1

        return Response(rep, status=status.HTTP_200_OK)


class CompraLecheSemana(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        serializer = VentasPorFechasSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            compras = Compra.objects.filter(fecha__range=[start_date, end_date])
            serializer_other = CompraSerializer(compras, many=True)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####### Nomina #######
class NominaDepartamentosApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Departaments
    """
    queryset = DepartamentoNom.objects.all()
    serializer_class = NominaDepartamentoSerializer


class NominaCargoApiView(viewsets.ReadOnlyModelViewSet):
    """_API for show the cargos_

    Args:
        viewsets (_type_): _description_
    """
    queryset = Cargo.objects.all()
    serializer_class = NominaCargoSerializer
    

# ¿Qué dia se vende más?
class DiaQueVendeMas(APIView):
    """
    API Día que más venden
    """
    
    def get(self, request):
        ahora = timezone.now()
        inicio_mes = ahora.replace(day=1, hour=1)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
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

        serializer = DiaQueMasVendeSerializar(ventas_mensuales, many=True)
        
        return Response(serializer.data)

    def post(self, request):
        serializer = AnnosMesVentasSerializer(data=request.data)
        zona_horaria = pytz.timezone('America/Havana')
        if serializer.is_valid():
            anno = serializer.validated_data['anno']
            mes = serializer.validated_data['mes']
            ahora = timezone.now()
            inicio_mes = ahora.replace(day=1, hour=1, month=mes, year=anno)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
            ventas_mensuales = Ventas.objects.filter(
                fecha__gte=inicio_mes,
                fecha__lte=fin_mes,
                id_producto__id_departamento__punto_de_venta=True
            ).values(
                'fecha' # , 'id_producto__id_departamento__departamento'
            ).annotate(
                venta_cantidad=Sum('cantidad'),
                venta_total=Sum('calculo')
            )
        
            # print(f"ventas_mensuales: {ventas_mensuales}")
        
            
            serializer = DiaQueMasVendeSerializar(ventas_mensuales, many=True)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DondeSeVendeMasAPI(APIView):
    """
    Dónde se vende más por día y por Puntos de Ventas
    """
    def post(self, request):
        serializer = AnnosMesVentasSerializer(data=request.data)
        zona_horaria = pytz.timezone('America/Havana')
        if serializer.is_valid():
            anno = serializer.validated_data['anno']
            mes = serializer.validated_data['mes']
            ahora = timezone.now()
            inicio_mes = ahora.replace(day=1, hour=1, month=mes, year=anno)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
            # Obtener ventas del mes actual
            ventas_mensuales = Ventas.objects.filter(
                fecha__gte=inicio_mes,
                fecha__lte=fin_mes,
                id_producto__id_departamento__punto_de_venta=True
            )

            # Crear un diccionario para almacenar los resultados
            resumen_mensual = {}

            # Inicializar el diccionario con los días y departamentos
            for i in range((fin_mes - inicio_mes).days + 1):
                dia = inicio_mes + timedelta(days=i)
                resumen_mensual[dia.strftime('%d')] = {}
                for departamento in Departamentos.objects.filter(punto_de_venta=True):
                    resumen_mensual[dia.strftime('%d')][departamento.departamento] = {
                        'cantidad_vendida': 0,
                        'total_vendido': 0
                    }

            print(resumen_mensual)
            # Rellenar el diccionario con los datos de ventas
            for venta in ventas_mensuales:
                dia = venta.fecha.strftime('%d')
                departamento = venta.id_producto.id_departamento.departamento
                resumen_mensual[dia][departamento]['cantidad_vendida'] += venta.cantidad
                resumen_mensual[dia][departamento]['total_vendido'] += venta.calculo

            # context['resumen_mensual'] = resumen_mensual
            # context['fecha'] =  inicio_mes
                
            serializer = DondeSeVendeMasSerializar(resumen_mensual, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnosDeVenta(APIView):
    """
    Años de Ventas
    """
    def get(self, request):
        # Annotate the queryset with the year extracted from the date field
        queryset = Ventas.objects.annotate(
            anno=ExtractYear('fecha')
        ).values('anno').annotate(
            cant_vendida=Count('id')
        ).order_by('anno')  # Order by year in descending order

        serializer = AnnosDeVentaSerializer(queryset, many=True)
        
        return Response(serializer.data)
    
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = AnnoSerializer(data=request.data)
        zona_horaria = pytz.timezone('America/Havana')
        if serializer.is_valid():
            anno = serializer.validated_data['anno']
            # ano = int(anno)
            inicio = datetime(anno, 1, 1, tzinfo=zona_horaria)
            fin = datetime(anno, 12, 31, tzinfo=zona_horaria)
            meses = Ventas.objects.filter(fecha__range=(inicio, fin)
                ).annotate(meses=TruncMonth('fecha')
                ).values('meses'
                ).annotate(ventas=Count('id')
                ).order_by('meses')
            serializer_other = MesesSerializer(meses, many=True)
            # return Response(ventas_fecha.values(), status=status.HTTP_200_OK)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaldoEfectivoView(viewsets.ReadOnlyModelViewSet):
# class SaldoEfectivoView(generics.ListAPIView):
    """
    Saldo Efectivo View
    """
    queryset = Cuenta.objects.get(cuenta="Efectivo")
    serializer_class = SaldoEfectivoSerializer
    # def get(self, request):
        # Filtrar la cuenta llamada "Efectivo"
        # efectivo = Cuenta.objects.filter(cuenta='Efectivo')
        # if efectivo:
        #     serializer = SaldoEfectivoSerializer(efectivo)
        #     return Response(serializer.data)
        # else:
        #     return Response({"error": "Cuenta Efectivo no se encuentra"}, status=404)
    def get_queryset(self):
        return Cuenta.objects.filter(cuenta='Efectivo')
    
    
class ContadorBilleteView(ViewSet):
    """
    Saldo Efectivo View
    """
    
    def list(self, request):
        registro = Contador_billete.objects.order_by('-id').first()
        serializer = CuentaBilletesSerializer(registro)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        registro = get_object_or_404(Contador_billete, id=pk)
        serializer = CuentaBilletesSerializer(registro)
        return Response(serializer.data)

class ContadorBilleteListView(viewsets.ReadOnlyModelViewSet):
    """
    Listado de Contador de Billetes View
    """
    queryset = Contador_billete.objects.all()
    serializer_class = ContadorBilleteListSerializer

# App Produccion
class ProduccionListView(viewsets.ReadOnlyModelViewSet):
    """
    Listado de Produccion View
    """
    queryset = Produccion.objects.all()
    serializer_class = ProduccionSerializer
    

class SalidaListView(viewsets.ReadOnlyModelViewSet):
    """
    Listado de Salida View
    """
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer 


class ProduccionProductoListView(viewsets.ReadOnlyModelViewSet):
    """
    Listado de Produccion Producto View
    """
    queryset = Producto.objects.all()
    serializer_class = ProduccionProductoSerializer


class CategoriaListView(viewsets.ReadOnlyModelViewSet):
    """
    Listado de Categoria View
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    