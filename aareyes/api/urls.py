from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import DepartamentoApiView, ProductoApiView, VentaApiView
from .views import VentasPorFechas

router = DefaultRouter()

router.register(prefix="departamentos", basename="departamentos", viewset=DepartamentoApiView)
router.register(prefix="productos", basename="productos", viewset=ProductoApiView)
router.register(prefix="ventas", basename="ventas", viewset=VentaApiView)
# router.register(prefix="ventas_fechas", viewset=VentasPorFechas.as_view(), basename="ventas_fechas")

urlpatterns = [
    path('ventas_fechas', VentasPorFechas.as_view(), name="ventas_fechas")
]
