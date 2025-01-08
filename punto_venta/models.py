from django.db import models
from django.utils import timezone
from django.db.models import Sum, F


# Create your models here.
class Cliente(models.Model):
    """
    Módulo Punto de Venta, Modelo Cliente
    """
    nombre = models.CharField(max_length=255, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]
        
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    """
    Módulo Punto de Venta, Modelo Proveedor
    """
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    correo = models.CharField(max_length=150, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Proveedore"
        verbose_name_plural = "Proveedores"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]
    
    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """
    Módulo Punto de Venta, Modelo Categoría
    """
    nombre = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Módulo Punto de Venta, Modelo Producto
    """
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
            # models.Index(fields=["sigla "]),
        ]

    def __str__(self):
        return self.nombre
    
    def inventario_en_almacen(self, almacen, fecha=None):
        if not fecha:
            fecha = timezone.now().date()

        entradas = Envio.objects.filter(producto=self, almacen=almacen, fecha__date__lte=fecha).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        salidas = Venta.objects.filter(producto=self, fecha__date__lte=fecha).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

        return self.cantidad + entradas - salidas

    def inventario_en_punto_de_venta(self, punto_de_venta, fecha=None):
        if not fecha:
            fecha = timezone.now().date()

        envios = Envio.objects.filter(producto=self, punto_de_venta=punto_de_venta, fecha__date__lte=fecha).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        ventas = Venta.objects.filter(producto=self, punto_de_venta=punto_de_venta, fecha__date__lte=fecha).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

        return envios - ventas


class Almacen(models.Model):
    """
    Módulo Punto de Venta, Modelo Almacen
    """
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
            # models.Index(fields=["sigla "]),
        ]

    def __str__(self):
        return self.nombre


class PuntoDeVenta(models.Model):
    """
    Módulo Punto de Venta, Modelo PuntoDeVenta
    """
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Punto_de_Venta"
        verbose_name_plural = "Puntos_de_Ventas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
            # models.Index(fields=["sigla "]),
        ]
        
    def __str__(self):
        return self.nombre


class Envio(models.Model):
    """
    Módulo Punto de Venta, Modelo Envio
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    punto_de_venta = models.ForeignKey(PuntoDeVenta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['producto']
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["producto"]),
            models.Index(fields=["punto_de_venta"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return f"{self.producto.nombre} enviado a {self.punto_de_venta.nombre}"


class Venta(models.Model):
    """
    Módulo Punto de Venta, Modelo Venta
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    punto_de_venta = models.ForeignKey(PuntoDeVenta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['producto']
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["producto"]),
            models.Index(fields=["punto_de_venta"]),
            models.Index(fields=["fecha"]),
        ]
    
    def __str__(self):
        return f"{self.cantidad} {self.producto.nombre} vendidos en {self.punto_de_venta.nombre}"
    