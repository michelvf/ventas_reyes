from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .views import ProduccionCreateView

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
]   