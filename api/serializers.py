from rest_framework import serializers
from ventas.models import Departamentos, Productos, Ventas, fileUpdate, Cuenta, Contador_billete, Tipo_cuenta
from compras.models import Almacen, Producto, PrecioProducto, Compra
from nomina.models import DepartamentoNom, Trabajador, Nomina, Cargo
from produccion.models import Categoria, Producto, Produccion, Salida, Destino
from django.db.models import Count


class FicherosSubidosSerializer(serializers.ModelSerializer):
    """
    Serializer for fileUpdate Model
    """
    class Meta:
        model = fileUpdate
        fields = ('id', 'fecha')


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer for Producto Model
    """

    class Meta:
        model = Productos
        fields = ("id", "codigo", "producto", "imagen", "id_departamento")


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


# class ProdMasVendidosSerializer(serializers.ModelSerializer):
class ProdMasVendidosSerializer(serializers.Serializer):
    """
    Products more sales, no se usa ModelSerializar porque la agrupación se hace
    en la consulta de la vista
    """
    cantidad_vendido = serializers.IntegerField()
    total_ventas = serializers.IntegerField()
    producto = serializers.CharField(source='id_producto__producto')
    #departamento = serializers.CharField(source='id_producto__id_departamento__departamento')
    

    # id_departamento=DepartamentoSerializer(
    #     read_only=True
    # )
    # id_producto=ProductoSerializer(
    #     read_only=True
    # )

    # class Meta:
    #     model = Ventas
    #     # fields  =["id_producto", "cantidad_vendido", "id_departamento", "total_ventas"]
    #     fields  =["id_producto", "cantidad_vendido", "total_ventas"]


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
    

class DondeSeVendeMasSerializar(serializers.Serializer):
    """
    Donde se vende más por día y por Puntos de Ventas
    """
    cantidad_vendida = serializers.DecimalField(max_digits=10, decimal_places=2) 
    total_vendido = serializers.DecimalField(max_digits=10, decimal_places=2)
    

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
    

# class SaldoEfectivoSerializer(serializers.Serializer):
class SaldoEfectivoSerializer(serializers.ModelSerializer):
    """
    Saldo de Efectivo Serializer
    """
    # saldo = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Cuenta
        fields = ['id',
                'cuenta',
                'saldo',
                'un_peso',
                'tres_pesos',
                'cinco_pesos',
                'diez_pesos',
                'veinte_pesos',
                'cincuenta_pesos',
                'cien_pesos',
                'doscientos_pesos',
                'quinientos_pesos',
                'mil_pesos'
                ]


class CuentaBilletesSerializer(serializers.ModelSerializer):
    """
    Saldo de Efectivo Serializer
    """
    # saldo = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Contador_billete
        fields = ['id',
                'total',
                'comentario',
                'un_peso',
                'tres_pesos',
                'cinco_pesos',
                'diez_pesos',
                'veinte_pesos',
                'cincuenta_pesos',
                'cien_pesos',
                'doscientos_pesos',
                'quinientos_pesos',
                'mil_pesos'
                ]


class TipoCuentaSerializer(serializers.ModelSerializer):
    """
    Listado de Tipos de Cuentas Serializer
    """
    class Meta:
        model = Tipo_cuenta
        fields = ['id', 'tipo', 'siglas']


class ContadorBilleteListSerializer(serializers.ModelSerializer):
    """
    Listado de Contador de Billetes Serializer
    """
    tipo_cuenta = TipoCuentaSerializer(read_only=True)

    class Meta:
        model = Contador_billete
        fields = ['id',
                'total',
                'sub_total',
                'comentario',
                'tipo_cuenta',
                'fecha'
                ]


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Listado de Categorias Serializer
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']


class ProduccionProductoSerializer(serializers.ModelSerializer):
    """
    Listado de Productos Serializer
    """
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'stock_actual']
    

class ProduccionSerializer(serializers.ModelSerializer):
    """
    Listado de Produccion Serializer
    """
    producto = ProduccionProductoSerializer(read_only=True)
    class Meta:
        model = Produccion
        fields = ['id', 'producto', 'cantidad', 'fecha_hora']
    

class DestinoSerializer(serializers.ModelSerializer):
    """
    Listado de Destinos Serializer
    """
    class Meta:
        model = Destino
        fields = ['id', 'nombre']


class SalidaSerializer(serializers.ModelSerializer):
    """
    Listado de Salida Serializer
    """
    producto = ProduccionProductoSerializer(read_only=True)
    destino = DestinoSerializer(read_only=True)
    class Meta:
        model = Salida
        fields = ['id', 'producto', 'cantidad', 'fecha_hora', 'destino']



    
