from django.contrib import admin
from .models import Almacen, Producto, UnidadMedida, Compra, PrecioProducto
from .models import Cliente, Producto, Factura, DetalleFactura

# Register your models here.
# class CompraAdmin(admin.ModelAdmin):
#    list_display = ['id', 'producto', 'cantidad', 'fecha', 'precio_compra']
#    search_fields = ['producto']


# class PrecioProductoAdmin(admin.ModelAdmin):
#    list_display = ['id', 'producto', 'precio', 'fecha']
#    search_fields = ['producto']


# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'nombre', 'medida', 'almacen', 'imagen']
#     search_fields = ['nombre']


class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'sigla']
    search_fields = ['nombre', 'sigla']


class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1
    readonly_fields = ['subtotal']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'ci', 'telefono', 'email', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'ci', 'email')
    list_filter = ('fecha_registro',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'fecha_actualizacion')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_filter = ('fecha_registro', 'fecha_actualizacion')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha_emision', 'subtotal', 'total', 'estado', 'cantidad_producto')
    list_filter = ('fecha_emision', 'estado')
    search_fields = ('numero', 'cliente__nombre', 'cliente__apellido', 'cliente__documento')
    readonly_fields = ('numero', 'subtotal', 'total')
    inlines = [DetalleFacturaInline]


@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('factura__fecha_emision',)
    search_fields = ('factura__numero', 'producto__nombre')
    readonly_fields = ['subtotal']


admin.site.register(Almacen, AlmacenAdmin)
# admin.site.register(Compra, CompraAdmin)
#admin.site.register(Producto, ProductoAdmin)
# admin.site.register(PrecioProducto, PrecioProductoAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
