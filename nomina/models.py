from django.db import models

# Create your models here.

class DepartamentoNom(models.Model):
    """
    Department Model
    """
    departamento = models.CharField(max_length=255, blank=False, null=False)
    comentario = models.TextField(blank=False, null=False)
    activo = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departamento']
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["departamento"]),
        ]

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    """
    Cargo Model
    """
    cargo = models.CharField(max_length=255, blank=False, null=False)
    comentario = models.TextField(blank=False, null=False)
    activo = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cargo']
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["cargo"]),
        ]

    def __str__(self):
        return self.cargo


class Trabajador(models.Model):
    """
    Worked model
    """
    nombre = models.CharField(max_length=255, blank=False, null=False)
    departamento = models.ForeignKey(DepartamentoNom,
        related_name="productos",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    activo = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Nomina(models.Model):
    """
    Payroll model
    """
    trabajador = models.ForeignKey(
        Trabajador,
        related_name="trabajdores",
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    salario = models.FloatField(blank=False, null=False)
    activo = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['trabajador']
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["trabajador"]),
            models.Index(fields=["salario"]),
        ]

    def __str__(self):
        return self.nombre

