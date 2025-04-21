from django.db import models
from django.utils import timezone


class Lacteos(models.Model):
    """
    Los Lácteos de la entidad
    """
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Lactetos"
        
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["nombre"]),
        ]        
    
    def __str__(self):
        return self.nombre


class fileUpdate(models.Model):
    """
    Modelo para saber la fecha de los ficheros que se han subido
    """
    archivo = models.FileField(upload_to='ficheros/')
    fecha = models.DateTimeField()
    actualizar = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha']
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return str(self.fecha.strftime("%Y-%m-%d"))


class Departamentos(models.Model):
    """
    Modelo para los Departamentos
    """
    departamento = models.CharField(max_length=200, null=False)
    comentario = models.TextField(blank=True, null=True)
    punto_de_venta = models.BooleanField(default=False)
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
    # codigo = models.IntegerField(null=False)  # Con Abarrote viejo
    codigo = models.CharField(max_length=400, null=False)  # Con Eleventa
    producto = models.CharField(max_length=200, null=False)
    imagen = models.ImageField(upload_to='ventas/', null=True, blank=True, default='ventas/defecto.jpg')
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


class Tipo_cuenta(models.Model):
    """
    Tipo de cuenta, de crédio o débito
    """
    tipo = models.CharField(max_length=100, blank=False, null=False)
    siglas = models.CharField(max_length=2, blank=False, null=False)
    comentario = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['tipo']
        verbose_name = "tipo_cuenta"
        verbose_name_plural = "tipo_cuentas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["tipo"]),
            models.Index(fields=["update_at"])
        ]

    def __str__(self):
        return self.tipo


class Cuenta(models.Model):
    """
    Saldo de las Cuentas Model
    """
    cuenta = models.CharField(max_length=100, null=False, blank=False)
    saldo = models.FloatField(null=False, blank=False)
    comentario = models.TextField(null=True, blank=True)
    un_peso = models.IntegerField(default=0)
    tres_pesos = models.IntegerField(default=0)
    cinco_pesos = models.IntegerField(default=0)
    diez_pesos = models.IntegerField(default=0)
    veinte_pesos = models.IntegerField(default=0)
    cincuenta_pesos = models.IntegerField(default=0)
    cien_pesos = models.IntegerField(default=0)
    doscientos_pesos = models.IntegerField(default=0)
    quinientos_pesos = models.IntegerField(default=0)
    mil_pesos = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['cuenta']
        verbose_name = "cuentas"
        verbose_name_plural = "cuentas"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["cuenta"]),
            models.Index(fields=["update_at"])
        ]

    def __str__(self):
        return self.cuenta


class Contador_billete(models.Model):
    """
    Modelo para registrara los conteos de billetes
    """
    comentario = models.TextField(null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_cuenta = models.ForeignKey(
        Tipo_cuenta,
        related_name="tipo_cuenta",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    un_peso = models.IntegerField(default=0, null=True, blank=True)
    tres_pesos = models.IntegerField(default=0, null=True, blank=True)
    cinco_pesos = models.IntegerField(default=0, null=True, blank=True)
    diez_pesos = models.IntegerField(default=0, null=True, blank=True)
    veinte_pesos = models.IntegerField(default=0, null=True, blank=True)
    cincuenta_pesos = models.IntegerField(default=0, null=True, blank=True)
    cien_pesos = models.IntegerField(default=0, null=True, blank=True)
    doscientos_pesos = models.IntegerField(default=0, null=True, blank=True)
    quinientos_pesos = models.IntegerField(default=0, null=True, blank=True)
    mil_pesos = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ["-fecha"] # ["-fecha"] ascending
        verbose_name = "contador_billete"
        verbose_name_plural = "contador_billetes"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["comentario"]),
            models.Index(fields=["total"]),
        ]

    def __str__(self):
        return f"{self.fecha.strftime('%d-%m-%Y')} - {self.comentario[:10]}"

"""
Notas:
02/12/24 4:13
El agregar el id_departamento al modelo Producto, hace que no haga falta en
modelo Ventas, y toda la relación se hace a través de producto, esto cambia
las consultas en las vistas, tantos en la app Ventas como en la API.
"""
