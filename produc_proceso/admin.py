from django.contrib import admin
from .models import Material, Producto, ProcesoProduccion, EntradaProduccion

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo_unitario', 'unidad_medida')
    search_fields = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta', 'costo_total', 'margen_ganancia')
    search_fields = ('nombre', 'descripcion')

class EntradaProduccionInline(admin.TabularInline):
    model = EntradaProduccion
    extra = 1

@admin.register(ProcesoProduccion)
class ProcesoProduccionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'fecha_inicio', 'estado', 'costo_total')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('producto__nombre', 'notas')
    inlines = [EntradaProduccionInline]

@admin.register(EntradaProduccion)
class EntradaProduccionAdmin(admin.ModelAdmin):
    list_display = ('proceso', 'material', 'cantidad', 'fecha', 'costo')
    list_filter = ('fecha', 'material')
    search_fields = ('proceso__producto__nombre', 'material__nombre')
