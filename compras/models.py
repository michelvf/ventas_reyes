from django.db import models

# Create your models here.
from django.utils import timezone


class UnidadMedida(models.Model):
    """
    Modelo para las Unidades de medida
    """
    nombre =  models.CharField(max_length=100)
    sigla = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "unidad_medida"
        verbose_name_plural = "unidades_medidas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
            # models.Index(fields=["sigla "]),
        ]

    def __str__(self):
        return self.nombre


class Almacen(models.Model):
    """
    Modelo para el Almacén
    """
    nombre = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "almacen"
        verbose_name_plural = "almacenes"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo para los Productos
    """
    nombre = models.CharField(max_length=100)
    medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='compras/', null=True, blank=True, default='/static/media/compras/defecto.jpg')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "producto"
        verbose_name_plural = "productos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return self.nombre


class PrecioProducto(models.Model):
    """
    Modelo para los Precios Productos
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['producto']
        verbose_name = "precio-producto"
        verbose_name_plural = "precios-productos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["producto"]),
            models.Index(fields=["precio"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return f"{self.producto.nombre} - {self.precio}"


class Compra(models.Model):
    """
    Modelo para las compras
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=timezone.now)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['producto']
        verbose_name = "compra"
        verbose_name_plural = "compras"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["producto"]),
            models.Index(fields=["cantidad"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return self.producto.nombre


class Cliente(models.Model):
    """
    Clients model
    """
    representante = models.CharField(max_length=200, null=False, blank=False)
    negocio = models.CharField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    telefono = models.CharField(max_length=200, null=True, blank=True)
    ci = models.IntegerField(max_length=11, min=11)
    autorizado = models.CharField(max_length=200, null=True, blank=True)
    ci = models.IntegerField()

    class Meta:
        ordering = ['representante']
        verbose_name = "cliene"
        verbose_name_plural = "clientes"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["represenante"]),
            models.Index(fields=["negocio"]),
            models.Index(fields=["telefono"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return self.representante