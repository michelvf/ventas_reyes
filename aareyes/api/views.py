import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import authentication
from ventas.models import Departamentos, Productos, Ventas, fileUpdate
from .serializers import DepartamentoSerializer, ProductoSerializer
from .serializers import VentaSerializer, VentasPorFechasSerializer
from .serializers import VentasPorFechasTodoSerializer, ProdxDepSerializer
from .serializers import ProdMasVendidosSerializer, SumarVentasPorFechasSerializer
from .serializers import ProdMasVendidosVarSerializer, LacteosSerializer
from .serializers import FicherosSubidosSerializer, VentaSemanalSerializer
from django.db.models import Sum, Count, Q, DateField
from django.db.models.functions import TruncDate, Substr
from django.utils import timezone
from datetime import timedelta, datetime


# Create your views here.
class ProductoApiView(viewsets.ReadOnlyModelViewSet):
    """
    API for show the Products
    """
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer


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
                .filter(productos__fecha__range=[start_date, end_date], id_departamento=departamento)
                .annotate(total_vendido=Sum('productos__cantidad'))
                .order_by('-total_vendido')[:10])
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
        lacteos = ['YOGUR','HELA','REQ','SUER','ENERG','PALE']
        condiciones = Q()
        for palabra in lacteos:
            condiciones |= Q(id_producto__producto__istartswith=palabra)
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
                 id_producto__id_departamento=departamento,
                 fecha__range=[start_date, end_date],
            ).values(
                'producto_s'
            ).annotate(
                total_vendido=Sum('cantidad'),
            #    codigo='id_producto__codigo',
            # ).order_by('total_vendido')
            ).order_by('producto_s')

            serializer_other = LacteosSerializer(lacteos_vendidos, many=True)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaSemanalAPI(APIView):
    """
    Ventas en la semana
    """
    def get(self, request):
        a_week = datetime.now() + timedelta(days=-36)

        week_sales = Ventas.objects.filter(
                fecha__gte=a_week
            ).annotate(
                fecha_agregada=TruncDate('fecha', output_field=DateField())
            ).values(
                'fecha_agregada'
            ).annotate(
                total_vendido=Sum('calculo')
            ).order_by('fecha_agregada')
            
        serializer = VentaSemanalSerializer(week_sales, many=True)
        
        return Response(serializer.data)