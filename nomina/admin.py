from django.contrib import admin

# Register your models here.
from nomina.models import DepartamentoNom, Trabajador, Nomina, Cargo


class DepartamentoNomAdmin(admin.ModelAdmin):
    list_display = ['id', 'departamento', 'comentario']
    search_fields = ['departamento']


class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cargo', 'comentario']
    search_fields = ['cargo']


admin.site.register(DepartamentoNom, DepartamentoNomAdmin)
admin.site.register(Cargo, CargoAdmin)
