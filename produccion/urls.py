from django.urls import path
from .views import ProductoListView, ProductoCreateView
from .views import ProduccionCreateView

urlpatterns = [
    ### Listdos
    path('productos/', ProductoListView.as_view(), name='productos_list'),
    path('productos/nuevos/', ProductoCreateView.as_view(), name='productos_nuevos'),
]