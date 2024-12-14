from django.db import models

# Create your models here.
from django.utils import timezone


class Almacen(models.Model):
    """
    Modelo para el Almacén
    """
    nombre = models.CharField(max_length=100)

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
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)

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
