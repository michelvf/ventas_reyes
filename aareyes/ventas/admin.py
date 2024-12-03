from django.contrib import admin

# Register your models here.
from .models import Productos, Ventas, Departamentos

class DepatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'departamento']
    search_fields = ['departamento']


class ProductAdmin(admin.ModelAdmin):
    list_display = ["codigo", "producto", "id_departamento"]
    # list_filter = ["codigo", "producto"]
    search_fields = ["codigo", "producto"]


class VentasAdmin(admin.ModelAdmin):
    list_display = ["id_producto", "cantidad", "venta", "costo", "fecha"]

admin.site.register(Productos, ProductAdmin)
admin.site.register(Departamentos, DepatoAdmin)
admin.site.register(Ventas, VentasAdmin)
