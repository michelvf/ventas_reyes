from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .views import ProduccionListView, ProduccionCreateView, ProduccionUpdateView, ProduccionDeleteView
from .views import DestinoListView, DestinoCreateView, DestinoUpdateView, DestinoDeleteView
from .views import SalidaListView, SalidaCreateView, SalidaUpdateView, SalidaDeleteView

urlpatterns = [
    ### Listdos
    path('productos/', ProductoListView.as_view(), name='productos_list'),
    path('productos/nuevos/', ProductoCreateView.as_view(), name='productos_nuevos'),
    path('productos/actualizar/<int:pk>/', ProductoUpdateView.as_view(), name='productos_actualizar'),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='productos_eliminar'),

    ### Categorías
    path('categorias/', CategoriaListView.as_view(), name='categorias_list'),
    path('categorias/nuevos/', CategoriaCreateView.as_view(), name='categorias_nuevos'),
    path('categorias/actualizar/<int:pk>/', CategoriaUpdateView.as_view(), name='categorias_actualizar'),
    path('categorias/eliminar/<int:pk>/', CategoriaDeleteView.as_view(), name='categorias_eliminar'),

    ### Producción
    path('produccion/', ProduccionListView.as_view(), name='produccion_list'),
    path('produccion/nuevos/', ProduccionCreateView.as_view(), name='produccion_nuevos'),
    path('produccion/actualizar/<int:pk>', ProduccionUpdateView.as_view(), name='produccion_actualizar'),
    path('produccion/eliminar/<int:pk>', ProduccionDeleteView.as_view(), name='produccion_eliminar'),
    
    ### Salida
    path('salida/', SalidaListView.as_view(), name='salida_list'),
    path('salida/nuevos/', SalidaCreateView.as_view(), name='salida_nuevos'),
    path('salida/actualizar/<int:pk>', SalidaUpdateView.as_view(), name='salida_actualizar'),
    path('salida/eliminar/<int:pk>', SalidaDeleteView.as_view(), name='salida_eliminar'),
    
    ### Destino
    path('destino/', DestinoListView.as_view(), name='destino_list'),
    path('destino/nuevos/', DestinoCreateView.as_view(), name='destino_nuevos'),
    path('destino/actualizar/<int:pk>', DestinoUpdateView.as_view(), name='destino_actualizar'),
    path('destino/eliminar/<int:pk>', DestinoDeleteView.as_view(), name='destino_eliminar'),
]   