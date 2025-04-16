from django.urls import path

from .views import barcode

urlpatterns = [
    # Listado
    path('crear/', barcode.as_view(), name='create-barcode'),
]