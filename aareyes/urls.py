"""
URL configuration for aareyes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from api.urls import router
from ventas.views import IndexView
from ventas import consumers

websocket_urlpatterns = [
    re_path(r'ws/datos/$', consumers.DatosConsumer.as_asgi()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name='index'),
    path("ventas/", include('ventas.urls')),
    path("api/", include(router.urls)),
    path("compras/", include('compras.urls')),
    # path("punto_venta/", include('punto_venta.urls')),
    path("nomina/", include('nomina.urls')),
    path("resumen/", include('resumen.urls')),
    path("barcode/", include('codigosbarra.urls')),
    path("produccion/", include('produccion.urls')),
    path("produc_proceso/", include('produc_proceso.urls')),
]

