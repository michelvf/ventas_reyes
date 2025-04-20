from django.contrib import admin

# Register your models here.
from .models import Productos, Ventas, Departamentos, fileUpdate, Contador_billete
from .models import Lacteos, Tipo_cuenta, Cuenta


class LacteosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion']
    search_fields = ['nombre']


class DepatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'departamento']
    search_fields = ['departamento']


class ProductAdmin(admin.ModelAdmin):
    list_display = ["codigo", "producto", "id_departamento", "imagen"]
    # list_filter = ["codigo", "producto"]
    search_fields = ["codigo", "producto"]


class VentasAdmin(admin.ModelAdmin):
    list_display = ["id_producto", "cantidad", "venta", "costo", "calculo", "fecha"]


class FicheroAdmin(admin.ModelAdmin):
    list_display = ["id", "fecha"]


class Tipo_cuentaAdmin(admin.ModelAdmin):
    list_display = ["id", "tipo", "siglas", "comentario"]


class CuentaAdmin(admin.ModelAdmin):
    list_display = ["id", "cuenta", "saldo", "comentario"]


admin.site.register(Productos, ProductAdmin)
admin.site.register(Departamentos, DepatoAdmin)
admin.site.register(Ventas, VentasAdmin)
admin.site.register(fileUpdate, FicheroAdmin)
admin.site.register(Contador_billete)
admin.site.register(Lacteos, LacteosAdmin)
admin.site.register(Tipo_cuenta, Tipo_cuentaAdmin)
admin.site.register(Cuenta, CuentaAdmin)
