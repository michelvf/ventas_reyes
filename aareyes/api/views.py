import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from ventas.models import Departamentos, Productos, Ventas
from .serializers import DepartamentoSerializer, ProductoSerializer
from .serializers import VentaSerializer, VentasPorFechasSerializer
from .serializers import VentasPorFechasTodoSerializer, ProdxDepSerializer
from .serializers import ProdMasVendidosSerializer, SumarVentasPorFechasSerializer
from .serializers import ProdMasVendidosVarSerializer
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta


# Create your views here.
class ProductoApiView(ModelViewSet):
    queryset = Productos.objects.all()
    # queryset = Productos.objects.values("codigo", "producto", "productos__cantidad")
    serializer_class = ProductoSerializer


class DepartamentoApiView(ModelViewSet):
    queryset = Departamentos.objects.all()
    # queryset = Departamentos.objects.values('departamento').annotate(cantidad=Count('departamentos__id'))
    serializer_class = DepartamentoSerializer


class VentaApiView(ModelViewSet):
    queryset = Ventas.objects.all()
    serializer_class = VentaSerializer


class VentasPorFechas(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = ProdMasVendidosVarSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            departamento = serializer.validated_data['departamento']
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
                .filter(productos__fecha__range=[start_date, end_date], id_departamento=1)
                .annotate(total_vendido=Sum('productos__cantidad'))
                .order_by('-total_vendido')[:10])
            serializer_other = ProdMasVendidosSerializer(produ_mas_vendido, many=True)
            return Response(serializer_other.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
