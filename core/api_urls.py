from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'api'

# URLs de la API REST de FilmScoper
urlpatterns = [
    
    # ============ ENDPOINTS DE PELÍCULAS ============
    # Lista y creación de películas
    path('peliculas/', 
         api_views.PeliculaListCreateAPIView.as_view(), 
         name='pelicula-list-create'),
    
    # Detalles, actualización y eliminación de película específica
    path('peliculas/<slug:slug>/', 
         api_views.PeliculaDetailAPIView.as_view(), 
         name='pelicula-detail'),
    
    # Películas por categoría
    path('peliculas/categoria/<slug:categoria_slug>/', 
         api_views.PeliculasPorCategoriaAPIView.as_view(), 
         name='peliculas-por-categoria'),
    
    # Búsqueda avanzada de películas
    path('buscar/', 
         api_views.buscar_peliculas, 
         name='buscar-peliculas'),
    
    
    # ============ ENDPOINTS DE RESEÑAS ============
    # Lista y creación de reseñas
    path('reseñas/', 
         api_views.ReseñaListCreateAPIView.as_view(), 
         name='reseña-list-create'),
    
    # Detalles, actualización y eliminación de reseña específica
    path('reseñas/<int:pk>/', 
         api_views.ReseñaDetailAPIView.as_view(), 
         name='reseña-detail'),
    
    # Reseñas por película específica
    path('reseñas/pelicula/<slug:pelicula_slug>/', 
         api_views.ReseñasPorPeliculaAPIView.as_view(), 
         name='reseñas-por-pelicula'),
    
    # Reseñas por usuario específico
    path('reseñas/usuario/<str:username>/', 
         api_views.ReseñasPorUsuarioAPIView.as_view(), 
         name='reseñas-por-usuario'),
    
    
    # ============ ENDPOINTS DE CATEGORÍAS ============
    # Lista de todas las categorías
    path('categorias/', 
         api_views.CategoriaListAPIView.as_view(), 
         name='categoria-list'),
    
    
    # ============ ENDPOINTS DE ESTADÍSTICAS ============
    # Estadísticas generales de películas
    path('estadisticas/peliculas/', 
         api_views.estadisticas_peliculas, 
         name='estadisticas-peliculas'),
    
    # Estadísticas del usuario autenticado
    path('estadisticas/usuario/', 
         api_views.estadisticas_usuario, 
         name='estadisticas-usuario'),
    
    
    # ============ ENDPOINTS DE SERVICIOS EXTERNOS ============
    # Búsqueda de portadas en TMDB
    path('tmdb/buscar-portadas/', 
         api_views.buscar_portadas_tmdb, 
         name='tmdb-buscar-portadas'),
    
    # Asignar portada de TMDB a película
    path('tmdb/asignar-portada/', 
         api_views.asignar_portada_tmdb, 
         name='tmdb-asignar-portada'),
    
    # Películas populares de TMDB
    path('tmdb/populares/', 
         api_views.peliculas_populares_tmdb, 
         name='tmdb-populares'),
    
    
    # ============ BROWSABLE API ROOT ============
    # Navegador de API de Django REST Framework
    path('', include('rest_framework.urls')),
]

"""
DOCUMENTACIÓN DE LA API REST DE FILMSCOPER

BASE URL: /api/

=== PELÍCULAS ===
GET    /api/peliculas/                           - Lista todas las películas (con filtros y paginación)
POST   /api/peliculas/                           - Crear nueva película (solo staff)
GET    /api/peliculas/{slug}/                    - Detalles de película específica
PUT    /api/peliculas/{slug}/                    - Actualizar película (solo staff)
DELETE /api/peliculas/{slug}/                    - Eliminar película (solo staff)
GET    /api/peliculas/categoria/{categoria}/     - Películas por categoría
GET    /api/buscar/                              - Búsqueda avanzada

Filtros disponibles para /api/peliculas/:
- ?search=termino                                - Búsqueda en título, director, reparto, sinopsis
- ?categorias__slug=accion                       - Filtrar por categoría
- ?año=2020                                      - Filtrar por año
- ?director=director                             - Filtrar por director
- ?ordering=-calificacion_promedio              - Ordenar por calificación (descendente)
- ?page=2                                        - Paginación

=== RESEÑAS ===
GET    /api/reseñas/                            - Lista todas las reseñas (con filtros)
POST   /api/reseñas/                            - Crear nueva reseña (requiere autenticación)
GET    /api/reseñas/{id}/                       - Detalles de reseña específica
PUT    /api/reseñas/{id}/                       - Actualizar reseña (solo autor)
DELETE /api/reseñas/{id}/                       - Eliminar reseña (solo autor)
GET    /api/reseñas/pelicula/{slug}/            - Reseñas de película específica
GET    /api/reseñas/usuario/{username}/         - Reseñas de usuario específico

Filtros disponibles para /api/reseñas/:
- ?pelicula__slug=pelicula-slug                 - Filtrar por película
- ?calificacion=5                               - Filtrar por calificación
- ?usuario__username=usuario                    - Filtrar por usuario
- ?ordering=-fecha_creacion                     - Ordenar por fecha

=== CATEGORÍAS ===
GET    /api/categorias/                         - Lista todas las categorías

=== ESTADÍSTICAS ===
GET    /api/estadisticas/peliculas/             - Estadísticas generales del sitio
GET    /api/estadisticas/usuario/               - Estadísticas del usuario autenticado

=== SERVICIOS EXTERNOS (TMDB) ===
GET    /api/tmdb/buscar-portadas/               - Buscar portadas en TMDB por título
POST   /api/tmdb/asignar-portada/               - Asignar portada de TMDB a película (solo staff)
GET    /api/tmdb/populares/                     - Obtener películas populares de TMDB

Parámetros para búsqueda de portadas:
- ?titulo=nombre_pelicula                       - Título de la película a buscar (requerido)
- ?año=2020                                     - Año para filtrar resultados (opcional)

=== FORMATOS DE RESPUESTA ===
Todas las APIs devuelven datos en formato JSON.
Las APIs de lista incluyen paginación automática.
Los errores siguen el formato estándar de Django REST Framework.

=== AUTENTICACIÓN ===
- Session Authentication: Para usuarios logueados en el sitio web
- Basic Authentication: Para acceso directo a la API
- Permisos: IsAuthenticatedOrReadOnly para la mayoría de endpoints
"""