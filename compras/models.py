from django.db import models
from ventas.models import Departamentos

# Create your models here.
from django.utils import timezone
import uuid


class PrecioProducto(models.Model):
    """
    Modelo para los Precios Productos
    """
    # producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)
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
    # producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)
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



class UnidadMedida(models.Model):
    """
    Modelo para las Unidades de medida de Facturación
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
    Modelo para el Almacén de Facturación
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


class Cliente(models.Model):
    """
    Modelo para Cliente de Facturación
    """
    
    def validar_longitud_11_digitos(value):
        if not (10000000000 <= value <= 99999999999):  # Rango válido para 11 dígitos
            raise ValidationError('El número debe tener exactamente 11 dígitos.')
    
    
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    # documento = models.CharField(max_length=20, unique=True)
    ci = models.IntegerField(validators=[validar_longitud_11_digitos])
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre', 'apellido']


class Producto(models.Model):
    """
    Modelo Producto de Facturación
    """
    codigo = models.CharField(max_length=250, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']


class Factura(models.Model):
    """
    Modelo para la Factura
    """
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('pagada-eleventa', 'Pagada y registrada en Eleventa'),
        ('anulada', 'Anulada'),
    )
    
    numero = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='facturas')
    fecha_emision = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonificacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = f"F-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def calcular_totales(self):
        detalles = self.detalles.all()
        self.subtotal = sum(detalle.subtotal for detalle in detalles)
        # self.iva = self.subtotal * 0.19  # IVA del 19%
        self.total = self.subtotal + self.bonificaion
        self.save()
    
    def __str__(self):
        return f"Factura #{self.numero} - {self.cliente}"
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_emision']


class DetalleFactura(models.Model):
    """
    Modeo para Detalle de la Factura
    """
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio histórico
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        # Si es un nuevo detalle, guardar el precio actual del producto
        if not self.pk:
            self.precio_unitario = self.producto.precio
        
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        
        super().save(*args, **kwargs)
        
        # Recalcular totales de la factura
        self.factura.calcular_totales()
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    class Meta:
        verbose_name = "Detalle de Factura"
        verbose_name_plural = "Detalles de Facturas"