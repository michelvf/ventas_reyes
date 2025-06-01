from django.db import models
from django.db.models import indexes


class Destino(models.Model):
    """
    Modelo Destino, de la app Producion
    """
    nombre = models.CharField(max_length=100, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return self.nombre
    


class Categoria(models.Model):
    """
    Modelo Categoría, de la app Producion
    """
    nombre = models.CharField(max_length=100, blank=False, null=False)
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
    Modelo Producto, de la app Produccion
    """
    nombre = models.CharField(max_length=255, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    stock_actual = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock_actual})"
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "producto"
        verbose_name_plural = "productos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
            models.Index(fields=["stock_actual"]),
        ]


class Produccion(models.Model):
    """
    Modelo Produccion, de la app Produccion
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} producidos el {self.fecha_hora}"
        
    class Meta:
        ordering = ['producto']
        verbose_name = "produccion"
        verbose_name_plural = "produccion"
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['producto']),
            models.Index(fields=['cantidad']),
        ]


class Salida(models.Model):
    """
    Modelo Salida, de la app Produccion
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} enviados a {self.destino}"

    def save(self, *args, **kwargs):
        # Disminuir stock al guardar
        if self.producto.stock_actual >= self.cantidad:
            self.producto.stock_actual -= self.cantidad
            self.producto.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("No hay suficiente stock disponible")
    
    class Meta:
        ordering = ['producto']
        verbose_name = 'salida'
        verbose_name_plural = 'salidas'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['producto']),
            models.Index(fields=['cantidad']),
        ]
