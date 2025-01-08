from django.contrib import admin
from .models import Producto, Envio, Venta, Almacen, PuntoDeVenta, Cliente

# Register your models here.

admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Envio)
admin.site.register(Cliente)
admin.site.register(Almacen)
admin.site.register(PuntoDeVenta)
