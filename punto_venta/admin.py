from django.contrib import admin
from .models import Producto, Transaccion, Venta, DetalleVenta, Cliente

# Register your models here.

admin.site.register(Producto)
admin.site.register(Transaccion)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Cliente)
