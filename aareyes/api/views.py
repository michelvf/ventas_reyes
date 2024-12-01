import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from ventas.models import Departamentos, Productos, Ventas
from .serializers import DepartamentoSerializer, ProductoSerializer
from .serializers import VentaSerializer, VentasPorFechasSerializer
from .serializers import VentasPorFechasTodoSerializer, SumarVentasPorFechas
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate


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
        serializer = VentasPorFechasSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
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
