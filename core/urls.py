from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Nueva ruta dinámica para categorías
    path('categoria/<slug:categoria_slug>/', views.categoria, name='categoria'),
    
    # Rutas específicas para compatibilidad
    path('accion/', views.accion, name='accion'),
    path('comedia/', views.comedia, name='comedia'),
    path('documentales/', views.documentales, name='documentales'),
    path('romantica/', views.romantica, name='romantica'),
    path('terror/', views.terror, name='terror'),
    
    # Autenticación
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('pelicula/', views.pelicula, name='pelicula'),
    
    # Listas personales
    path('mis-favoritos/', views.mis_favoritos, name='mis_favoritos'),
    path('ver-mas-tarde/', views.ver_mas_tarde_lista, name='ver_mas_tarde_lista'),
    
    # APIs para funcionalidades AJAX
    path('api/calificar/<int:pelicula_id>/', views.calificar_pelicula, name='calificar_pelicula'),
    path('api/favorito/<int:pelicula_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('api/ver-mas-tarde/<int:pelicula_id>/', views.toggle_ver_mas_tarde, name='toggle_ver_mas_tarde'),
    
    # Nuevas APIs para listas personales
    path('toggle-favorito/<int:pelicula_id>/', views.toggle_favorito, name='toggle_favorito_nuevo'),
    path('toggle-ver-mas-tarde-nuevo/<int:pelicula_id>/', views.toggle_ver_mas_tarde_nuevo, name='toggle_ver_mas_tarde_nuevo'),
]