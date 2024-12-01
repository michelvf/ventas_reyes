from rest_framework import serializers
from ventas.models import Departamentos, Productos, Ventas
# from django.db import models


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer for Departamentos Model 
    """
    # cantidad = serializers.IntegerField(read_only=True)

    class Meta:
        model = Departamentos
        # fields = ("id", "departamento", "cantidad")
        fields = ("id", "departamento")


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer for Productos Model 
    """
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Productos
        fields = ("id", "codigo", "producto", "total")


class VentaSerializer(serializers.ModelSerializer):
    """
    Serializer for Ventas Model 
    """

    departamento=DepartamentoSerializer(
        read_only=True
    )

    producto=ProductoSerializer(
        # many=True,
        read_only=True
    )

    class Meta:
        model = Ventas
        fields = ("id", "producto", "cantidad", "costo", "venta", "calculo", "departamento", "fecha")


class VentasPorFechasSerializer(serializers.Serializer):
    """
    Serializer for Ventas with dates
    """
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class VentasPorFechasTodoSerializer(serializers.ModelSerializer):
    """
    Serializer for filter bettwen dates
    """
    departamento=DepartamentoSerializer(
        read_only=True
    )

    producto=ProductoSerializer(
        # many=True,
        read_only=True
    )

    class Meta:
        model = Ventas
        fields = ("id", "producto", "cantidad", "costo", "venta", "calculo", "departamento", "fecha")


class SumarVentasPorFechas(serializers.ModelSerializer):
    """
    Serializer for Sum calculo bettwen dates
    """
    suma = serializers.FloatField()

    class Meta:
        model = Ventas
        field = ("suma", "fecha")
