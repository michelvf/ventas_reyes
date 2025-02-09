from django.contrib import admin
from .models import ResumenVentas

# Register your models here.
class ResumenVentasAdmin(admin.ModelAdmin):
    list_display = ['id', 'periodo', 'total_vendido', 'fecha_actualizacion']


admin.site.register(ResumenVentas, ResumenVentasAdmin)