from django.db import models

# Create your models here.
class ResumenVentas(models.Model):
    """
    Modelo Resumen de las Ventas, va a guardar las ventas en el tiempo
    """
    periodo = models.CharField(max_length=100)
    total_vendido = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["fecha_actualizacion"] # ["-fecha"] ascending
        verbose_name = "ResumenVenta"
        verbose_name_plural = "ResumenVentas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha_actualizacion"]),
        ]
    
    def __str__(self):
        return self.periodo
    

class Estadisticas(models.Model):
    tipo = {
        "s": "Semanal",
        "M": "Mensual",
        "T": "Trimestral",
        "S": "Semestral",
        "A": "Anual",
    }
    tipos = models.CharField(max_length=1, choices=tipo)
    periodo = models.CharField(max_length=100)
    total_vendido = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["fecha_actualizacion"] # ["-fecha"] ascending
        verbose_name = "ResumenVenta"
        verbose_name_plural = "ResumenVentas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha_actualizacion"]),
        ]
    
    def __str__(self):
        return self.periodo