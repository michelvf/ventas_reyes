from django.contrib import admin
from .models import Almacen, Producto, Compra, PrecioProducto, UnidadMedida

# Register your models here.
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'cantidad', 'fecha', 'precio_compra']
    search_fields = ['producto']


class PrecioProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'producto', 'precio', 'fecha']
    search_fields = ['producto']


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'medida', 'almacen', 'imagen']
    search_fields = ['nombre']


class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'sigla']
    search_fields = ['nombre', 'sigla']


admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(PrecioProducto, PrecioProductoAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
