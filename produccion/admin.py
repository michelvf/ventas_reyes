from django.contrib import admin

# Register your models here.
from .models import Categoria, Producto, Produccion, Salida, Destino

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Produccion)
admin.site.register(Salida)
admin.site.register(Destino)


