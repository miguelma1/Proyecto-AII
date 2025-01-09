from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('poblar_base_datos/', views.poblar_base_datos, name='poblar_base_datos'),
    path('listar_ropa_hombre/', views.lista_ropa_hombre, name='lista_ropa_hombre'),
    path('listar_ropa_hombre_rebajada/', views.lista_ropa_hombre_rebajada, name='lista_ropa_hombre_rebajada'),
    path('buscar_ropa_hombre/', views.buscar_ropa_hombre, name='buscar_ropa_hombre'),
    path('indexar_datos/', views.indexar_datos, name='indexar_datos'),
    path('buscar_precio/', views.buscar_precio, name='buscar_precio'),

    ]
"""
    path('',views.index),
    path('populate/', views.populateDatabase), 
    path('denominacion_vinos/',views.mostrar_vinos_por_denominaciones),
    path('vinos_anyo/',views.buscar_vinos_por_anyo),
    path('vinos_uva/',views.buscar_vinos_por_uva),
    path('admin/', admin.site.urls),
    """