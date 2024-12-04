from rest_framework import serializers
from ventas.models import Departamentos, Productos, Ventas
from django.db.models import Count


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer for Departamentos Model 
    """

    class Meta:
        model = Departamentos
        # fields = ("id", "departamento", "cantidad")
        fields = ("id", "departamento")


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer for Productos Model 
    """

    id_departamento=DepartamentoSerializer(
        read_only=True
    )

    class Meta:
        model = Productos
        fields = ("id", "codigo", "producto", "id_departamento")


class VentaSerializer(serializers.ModelSerializer):
    """
    Serializer for Ventas Model 
    """

    id_producto=ProductoSerializer(
        # many=True,
        read_only=True
    )

    class Meta:
        model = Ventas
        fields = ("id", "id_producto", "cantidad", "costo", "venta", "calculo", "fecha")


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
    # departamento=DepartamentoSerializer(
    #     read_only=True
    # )

    id_producto=ProductoSerializer(
        # many=True,
        read_only=True
    )

    class Meta:
        model = Ventas
        fields = ("id", "id_producto", "cantidad", "costo", "venta", "calculo", "fecha")


class SumarVentasPorFechasSerializer(serializers.ModelSerializer):
    """
    Serializer for Sum calculo bettwen dates
    """
    suma = serializers.FloatField()

    class Meta:
        model = Ventas
        fields = ("suma", "fecha")


class ProdxDepSerializer(serializers.ModelSerializer):
    """
    Products x Departament
    """
    num_prod = serializers.IntegerField()

    class Meta:
        model = Departamentos
        fields = ("id", "departamento", "num_prod")

class ProdMasVendidosVarSerializer(serializers.Serializer):
    """
    Serializer for Ventas with dates
    """
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    departamento = serializers.IntegerField()


class ProdMasVendidosSerializer(serializers.ModelSerializer):
    """
    Products more sales
    """
    total_vendido = serializers.IntegerField()

    id_departamento=DepartamentoSerializer(
        read_only=True
    )

    class Meta:
        model = Productos
        fields  =["codigo", "producto", "total_vendido", "id_departamento"]
