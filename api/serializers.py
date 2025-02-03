from rest_framework import serializers
from ventas.models import Departamentos, Productos, Ventas, fileUpdate
from compras.models import Almacen, Producto, PrecioProducto, Compra
from nomina.models import DepartamentoNom, Trabajador, Nomina, Cargo
from django.db.models import Count


class FicherosSubidosSerializer(serializers.ModelSerializer):
    """
    Serializer for fileUpdate Model
    """
    class Meta:
        model = fileUpdate
        fields = ('id', 'fecha')


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer for Departamentos Model 
    """

    class Meta:
        model = Departamentos
        fields = ("id", "departamento", "comentario", "punto_de_venta")


class ProductosSerializer(serializers.ModelSerializer):
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

    id_producto=ProductosSerializer(
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
    id_producto=ProductosSerializer(
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
    
    def id_puntoVenta():
        id = [dep.id for dep in Departamentos.objects.all()]
        return id
    
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    # departamento = serializers.IntegerField()
    departamento = serializers.MultipleChoiceField(choices=id_puntoVenta())


class ProdMasVendidosSerializer(serializers.ModelSerializer):
    """
    Products more sales
    """
    total_vendido = serializers.IntegerField()
    total_ventas = serializers.IntegerField()

    id_departamento=DepartamentoSerializer(
        read_only=True
    )

    class Meta:
        model = Productos
        fields  =["codigo", "producto", "total_vendido", "id_departamento", "total_ventas"]


class LacteosSerializer(serializers.ModelSerializer):
    """docstring for LacteosSerializer"""
    
    total_vendido = serializers.IntegerField()
    producto_s = serializers.CharField()
    total_ventas = serializers.IntegerField()

    id_producto=ProductosSerializer(
        # many=True,
        read_only=True
    )
    

    class Meta:
        model = Ventas
        fields = ["id_producto", "total_vendido", "producto_s", "total_ventas"]


class VentaSemanalSerializer(serializers.Serializer): 
    """
    Product selling in a week
    """
    fecha_agregada = serializers.DateField()
    total_vendido = serializers.DecimalField(max_digits=10, decimal_places=2) 
    
    # id_producto = ProductoSerializer(
    #     read_only=True
    # )

    # class Meta:
    #     model = Ventas
    #     fields = ["fecha", "total_vendido"]

######### Compra ############################
class AlmacenSerializer(serializers.ModelSerializer):
    """
    Serializer for Almacen Model
    """
    class Meta:
        model = Almacen
        fields = ('id', 'nombre')


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer for Producto Model
    """
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'almacen')


class PrecioProductoSerializer(serializers.ModelSerializer):
    """
    Serializer for PrecioProducto Model
    """
    class Meta:
        model = PrecioProducto
        fields = ('id', 'producto', 'precio', 'fecha')


class CompraSerializer(serializers.ModelSerializer):
    """
    Serializer for Compra Model
    """
    class Meta:
        model = Compra
        fields = ('id', 'producto', 'cantidad', 'precio_compra', 'fecha')


class NominaDepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer for Departament Paypull
    """
    class Meta:
        model = DepartamentoNom
        fields = ('id', 'departamento', 'comentario')


class NominaCargoSerializer(serializers.ModelSerializer):
    """
    Serializer for Cargo Paypull
    """
    class Meta:
        model = Cargo
        fields = ('id', 'cargo', 'comentario')
        

class DiaQueMasVendeSerializar(serializers.Serializer):
    """
    Serializer for more Sales by Days
    """
    fecha = serializers.DateTimeField()
    venta_cantidad = serializers.DecimalField(max_digits=10, decimal_places=2) 
    venta_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    

class AnnosDeVentaSerializer(serializers.Serializer):
    """
    Años de Ventas
    """
    anno = serializers.IntegerField()
    cant_vendida = serializers.IntegerField()


class AnnoSerializer(serializers.Serializer):
    """
    Serializer for Ventas with year
    """
    anno = serializers.IntegerField()


class MesesSerializer(serializers.Serializer):
    """
    Meses de Ventas
    """
    meses = serializers.DateTimeField()
    ventas = serializers.IntegerField()


class AnnosMesVentasSerializer(serializers.Serializer):
    """
    Años de Ventas
    """
    anno = serializers.IntegerField()
    mes = serializers.IntegerField()