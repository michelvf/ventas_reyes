from django.contrib import admin

# Register your models here.
from .models import Productos, Ventas, Departamentos

class ProductAdmin(admin.ModelAdmin):
    list_display = ["codigo", "producto"]
    # list_filter = ["codigo", "producto"]
    search_fields = ["codigo", "producto"]


class VentasAdmin(admin.ModelAdmin):
    list_display = ["producto", "cantidad", "venta", "costo", "departamento", "fecha"]

admin.site.register(Productos, ProductAdmin)
admin.site.register(Departamentos)
admin.site.register(Ventas, VentasAdmin)
