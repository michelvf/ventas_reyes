from django.urls import path
from . import views

app_name = 'produc_proceso'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Productos
    path('produc_producto/', views.ProductoListView.as_view(), name='producto_lista'),
    path('produc_producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detalle'),
    path('produc_producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('produc_producto/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    
    # Materiales
    path('materiales/', views.MaterialListView.as_view(), name='material_lista'),
    path('materiales/nuevo/', views.MaterialCreateView.as_view(), name='material_crear'),
    path('materiales/<int:pk>/editar/', views.MaterialUpdateView.as_view(), name='material_editar'),
    
    # Procesos de Producción
    path('procesos/', views.ProcesoListView.as_view(), name='proceso_lista'),
    path('procesos/nuevo/', views.ProcesoCreateView.as_view(), name='proceso_crear'),
    path('procesos/<int:pk>/', views.ProcesoDetailView.as_view(), name='proceso_detalle'),
    path('procesos/<int:pk>/editar/', views.ProcesoUpdateView.as_view(), name='proceso_editar'),
    path('procesos/<int:pk>/finalizar/', views.ProcesoFinalizarView.as_view(), name='proceso_finalizar'),
    
    # Entradas de Producción
    path('procesos/<int:proceso_id>/entradas/nueva/', views.EntradaCreateView.as_view(), name='entrada_crear'),
    path('entradas/<int:pk>/editar/', views.EntradaUpdateView.as_view(), name='entrada_editar'),
    path('entradas/<int:pk>/eliminar/', views.EntradaDeleteView.as_view(), name='entrada_eliminar'),
    
    # API para DataTables
    path('api/productos/', views.ProductoAPIView.as_view(), name='api_productos'),
    path('api/procesos/', views.ProcesoAPIView.as_view(), name='api_procesos'),
    path('api/entradas/<int:proceso_id>/', views.EntradaAPIView.as_view(), name='api_entradas'),
]
