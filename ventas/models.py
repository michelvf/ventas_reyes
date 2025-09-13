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
        ordering = ['-fecha']
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
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"
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
        null=False,
        db_index=True
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
        Productos,
        related_name='productos',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        db_index=True
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


# class Moneda(models.Model):
#     """
#     Modelo Monedas
#     """
#     nombre = models.CharField(max_length=100, blank=False, null=False)
#     sigla = models.CharField(max_length=3, blank=False, null=False)
#     comentario = models.TextField(null=True, blank=True)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['sigla']
#         verbose_name = 'moneda'
#         verbose_name_plural = 'monedas'
#         indexes = [
#             models.Index(fields=["sigla"]),
#         ]
    
#     def __str__(self):
#         return self.sigla


class Tipo_cuenta(models.Model):
    """
    Modelo Tipo de cuenta, de crédio o débito
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
        return self.siglas


class Cuenta(models.Model):
    """
    Saldo de las Cuentas Model
    """
    cuenta = models.CharField(max_length=100, null=False, blank=False)
    saldo = models.FloatField(null=False, blank=False)
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
    comentario = models.TextField(null=True, blank=True)
    # moneda = models.ForeignKey(
    #     Moneda,
    #     on_delete=models.CASCADE,
    #     # default=1
    # )
    # moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    #    related_name='monedas',    
    #    blank=False,
    #    null=False,
    #    db_index=True,
    #    default='CUP'
    #)
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

    # def save(self, *args, **kwargs):
    #     previo = Cuenta.objects.get(cuenta="Efectivo")
    #     registro = Contador_billete(
    #         historia=1,
    #         un_peso=getattr(self, 'un_peso'),
    #         tres_pesos=getattr(self, 'tres_pesos'),
    #         cinco_pesos=getattr(self, 'cinco_pesos'),
    #         diez_pesos=getattr(self, 'diez_pesos'),
    #         veinte_pesos=getattr(self, 'veinte_pesos'),
    #         cincuenta_pesos=getattr(self, 'cincuenta_pesos'),
    #         cien_pesos=getattr(self, 'cien_pesos'),
    #         doscientos_pesos=getattr(self, 'doscientos_pesos'),
    #         quinientos_pesos=getattr(self, 'quinientos_pesos'),
    #         mil_pesos=getattr(self, 'mil_pesos'),
    #         total=0,
    #         sub_total=getattr(self, 'saldo'),
    #         comentario="Historial",
    #     )
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.cuenta


class Contador_billete(models.Model):
    """
    Modelo para registrar los conteos de billetes
    """
    comentario = models.TextField(null=False, blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_cuenta = models.ForeignKey(
        Tipo_cuenta,
        related_name="tipos_cuentas",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        db_index=True
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
    sub_total = models.IntegerField(null=False, blank=False)
    historia = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"] # ["-fecha"] ascending
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


class Cuenta_historico(models.Model):
    """
    Modelo para registrar lo que se guarda en Cuentas
    """
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
    # saldo = models.IntegerField(null=False, blank=False)
    saldo = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha"] # ["-fecha"] ascending
        verbose_name = "cuenta_historico"
        verbose_name_plural = "cuentas_historico"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["saldo"]),
        ]

    def __str__(self):
        return f"{self.fecha.strftime('%d-%m-%Y')}"

# class RegistroLog(models.Model):
#     registro       = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='logs')
#     campo          = models.CharField(max_length=50)
#     valor_antiguo  = models.TextField()
#     valor_nuevo    = models.TextField()
#     fecha          = models.DateTimeField()


"""
Notas:
02/12/24 4:13
El agregar el id_departamento al modelo Producto, hace que no haga falta en
modelo Ventas, y toda la relación se hace a través de producto, esto cambia
las consultas en las vistas, tantos en la app Ventas como en la API.

ALTER TABLE ventas_cuenta ADD COLUMN moneda_id INTEGER REFERENCES moneda(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ventas_contador_billete ADD COLUMN historia TEXT;
"""
