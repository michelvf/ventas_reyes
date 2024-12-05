from django.db import models


class fileUpdate(models.Model):
    """
    Modelo para saber la fecha de los ficheros que se han subido
    """
    fecha = models.DateTimeField()

    class Meta:
        ordering = ['fecha']
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return self.fecha


class Departamentos(models.Model):
    """
    Modelo para los Departamentos
    """
    departamento = models.CharField(max_length=200, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "departmento"
        verbose_name_plural = "departmentos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["departamento"]),
        ]

    def __str__(self):
        return self.departamento


class Productos(models.Model):
    """
    Modelo para los Productos
    """
    codigo = models.IntegerField(null=False)
    producto = models.CharField(max_length=200, null=False)
    id_departamento = models.ForeignKey(
        Departamentos,
        related_name="productos",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["producto"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["codigo"]),
            models.Index(fields=["producto"]),
        ]

    def __str__(self):
        return self.producto


class Ventas(models.Model):
    """
    Modelo para las Ventas
    """
    id_producto = models.ForeignKey(
    # producto = models.ForeignKey(
        Productos,
        related_name='productos',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    cantidad = models.FloatField(null=False)
    venta = models.FloatField(null=False)
    costo = models.FloatField(null=False)
    calculo = models.FloatField(null=False)
    fecha = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha"] # ["-fecha"] ascending
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["id_producto"]),
            models.Index(fields=["calculo"]),
        ]

    def __str__(self):
        return self.id_producto.producto

"""
Notas:
02/12/24 4:13
El agregar el id_departamento al modelo Producto, hace que no haga falta en
modelo Ventas, y toda la relación se hace a través de producto, esto cambia
las consultas en las vistas, tantos en la app Ventas como en la API.
"""
