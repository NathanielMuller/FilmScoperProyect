from django.urls import path
from . import views, tmdb_views

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
    
    # URLs para integración TMDB (solo para staff)
    path('tmdb/buscar-portadas/', tmdb_views.buscar_portadas_admin, name='tmdb_buscar_portadas'),
    path('tmdb/agregar-pelicula/', tmdb_views.agregar_pelicula_con_tmdb, name='tmdb_agregar_pelicula'),
    path('tmdb/ajax/buscar-portadas/', tmdb_views.ajax_buscar_portadas, name='tmdb_ajax_buscar'),
    path('tmdb/ajax/asignar-portada/', tmdb_views.ajax_asignar_portada, name='tmdb_ajax_asignar'),
    path('tmdb/ajax/obtener-detalles/', tmdb_views.ajax_obtener_detalles_completos, name='tmdb_ajax_detalles'),
    path('tmdb/ajax/usage-counter/', tmdb_views.ajax_tmdb_usage_counter, name='tmdb_ajax_usage_counter'),
    
    # URLs para integración YouTube (solo para staff)
    path('youtube/ajax/buscar-trailer/', tmdb_views.ajax_buscar_trailer_youtube, name='youtube_ajax_buscar_trailer'),
    path('youtube/ajax/detalles-trailer/', tmdb_views.ajax_obtener_detalles_trailer, name='youtube_ajax_detalles_trailer'),
]