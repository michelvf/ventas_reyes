from django.db import models
from django.utils import timezone
from django.db.models import Sum, F

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    def costo_total(self):
        """Calcula el costo total acumulado de todos los materiales usados en este producto"""
        procesos = self.procesoproduccion_set.all()
        costo = 0
        for proceso in procesos:
            costo += proceso.costo_total()
        return costo
    
    def margen_ganancia(self):
        """Calcula el margen de ganancia basado en el precio de venta y el costo total"""
        costo = self.costo_total()
        if costo > 0:
            return ((self.precio_venta - costo) / costo) * 100
        return 0
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class ProcesoProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('iniciado', 'Iniciado'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ], default='iniciado')
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Proceso de {self.producto.nombre} - {self.fecha_inicio}"
    
    def costo_total(self):
        """Calcula el costo total de todas las entradas de producción para este proceso"""
        resultado = self.entradaproduccion_set.aggregate(
            total=Sum(F('cantidad') * F('material__costo_unitario'))
        )
        return resultado['total'] or 0
    
    def materiales_usados(self):
        """Retorna un queryset con todos los materiales usados en este proceso"""
        return Material.objects.filter(entradaproduccion__proceso=self).distinct()
    
    class Meta:
        verbose_name = "Proceso de Producción"
        verbose_name_plural = "Procesos de Producción"

class EntradaProduccion(models.Model):
    proceso = models.ForeignKey(ProcesoProduccion, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.cantidad} {self.material.unidad_medida} de {self.material.nombre} para {self.proceso.producto.nombre}"
    
    def costo(self):
        """Calcula el costo de esta entrada basado en la cantidad y el costo unitario del material"""
        return self.cantidad * self.material.costo_unitario
    
    class Meta:
        verbose_name = "Entrada de Producción"
        verbose_name_plural = "Entradas de Producción"
