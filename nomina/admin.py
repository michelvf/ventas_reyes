from django.contrib import admin

# Register your models here.
from nomina.models import DepartamentoNom, Trabajador, Nomina, Cargo


class DepartamentoNomAdmin(admin.ModelAdmin):
    list_display = ['id', 'departamento', 'comentario']
    search_fields = ['departamento']


class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cargo', 'comentario']
    search_fields = ['cargo']
    

class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'departamento', 'cargo']
    search_fields = ['nombre']


class NominaAdmin(admin.ModelAdmin):
    list_display = ['id', 'trabajador', 'salario', 'activo']
    search_fields = ['trabajador']

admin.site.register(DepartamentoNom, DepartamentoNomAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Trabajador, TrabajadoresAdmin)
admin.site.register(Nomina, NominaAdmin)
