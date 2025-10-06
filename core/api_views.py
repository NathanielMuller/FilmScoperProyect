from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404

from .models import Pelicula, Categoria, Reseña, ComentarioPelicula
from .serializers import (
    PeliculaListSerializer, PeliculaDetailSerializer, PeliculaCreateSerializer,
    ReseñaSerializer, ReseñaCreateSerializer, CategoriaSerializer,
    ComentarioPeliculaSerializer, PeliculaStatsSerializer, UsuarioStatsSerializer
)
from .services import tmdb_service, youtube_service


class StandardResultsSetPagination(PageNumberPagination):
    """Paginación personalizada para APIs"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50


# ============ APIS DE PELÍCULAS ============

class PeliculaListCreateAPIView(generics.ListCreateAPIView):
    """
    Lista todas las películas activas o crea una nueva película
    GET: /api/peliculas/
    POST: /api/peliculas/ (requiere autenticación de staff)
    """
    queryset = Pelicula.objects.filter(activa=True)
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorias__slug', 'año', 'director']
    search_fields = ['titulo', 'director', 'reparto', 'sinopsis']
    ordering_fields = ['fecha_agregada', 'calificacion_promedio', 'año', 'titulo']
    ordering = ['-fecha_agregada']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PeliculaCreateSerializer
        return PeliculaListSerializer
    
    def get_permissions(self):
        """Solo staff puede crear películas"""
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Validar que solo staff pueda crear películas"""
        if not self.request.user.is_staff:
            raise PermissionDenied("Solo el staff puede crear películas")
        serializer.save()


class PeliculaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina una película específica
    GET: /api/peliculas/{id}/
    PUT/PATCH: /api/peliculas/{id}/ (requiere staff)
    DELETE: /api/peliculas/{id}/ (requiere staff)
    """
    queryset = Pelicula.objects.filter(activa=True)
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PeliculaCreateSerializer
        return PeliculaDetailSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Solo el staff puede modificar películas")
        serializer.save()
    
    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("Solo el staff puede eliminar películas")
        # Soft delete - marcar como inactiva en lugar de eliminar
        instance.activa = False
        instance.save()


class PeliculasPorCategoriaAPIView(generics.ListAPIView):
    """
    Lista películas de una categoría específica
    GET: /api/peliculas/categoria/{categoria_slug}/
    """
    serializer_class = PeliculaListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'director', 'reparto']
    ordering_fields = ['fecha_agregada', 'calificacion_promedio', 'año']
    ordering = ['-fecha_agregada']
    
    def get_queryset(self):
        categoria_slug = self.kwargs['categoria_slug']
        return Pelicula.objects.filter(
            categorias__slug=categoria_slug, 
            activa=True
        ).distinct()


# ============ APIS DE RESEÑAS ============

class ReseñaListCreateAPIView(generics.ListCreateAPIView):
    """
    Lista reseñas o crea una nueva reseña
    GET: /api/reseñas/
    POST: /api/reseñas/ (requiere autenticación)
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pelicula__slug', 'calificacion', 'usuario__username']
    ordering_fields = ['fecha_creacion', 'calificacion']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        return Reseña.objects.filter(activa=True).select_related('usuario', 'pelicula')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReseñaCreateSerializer
        return ReseñaSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Verificar si el usuario ya reseñó esta película
        pelicula = serializer.validated_data['pelicula']
        if Reseña.objects.filter(
            usuario=self.request.user, 
            pelicula=pelicula, 
            activa=True
        ).exists():
            raise ValidationError(
                "Ya has reseñado esta película. Puedes editarla en lugar de crear una nueva."
            )
        
        reseña = serializer.save()
        # Actualizar calificación promedio de la película
        pelicula.actualizar_calificacion()


class ReseñaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtiene, actualiza o elimina una reseña específica
    GET: /api/reseñas/{id}/
    PUT/PATCH: /api/reseñas/{id}/ (solo el autor)
    DELETE: /api/reseñas/{id}/ (solo el autor)
    """
    serializer_class = ReseñaSerializer
    
    def get_queryset(self):
        return Reseña.objects.filter(activa=True).select_related('usuario', 'pelicula')
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def perform_update(self, serializer):
        # Solo el autor puede modificar su reseña
        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied("Solo puedes modificar tus propias reseñas")
        
        reseña = serializer.save()
        # Actualizar calificación de la película
        reseña.pelicula.actualizar_calificacion()
    
    def perform_destroy(self, instance):
        if instance.usuario != self.request.user:
            raise PermissionDenied("Solo puedes eliminar tus propias reseñas")
        
        pelicula = instance.pelicula
        instance.delete()
        # Actualizar calificación de la película
        pelicula.actualizar_calificacion()


class ReseñasPorPeliculaAPIView(generics.ListAPIView):
    """
    Lista reseñas de una película específica
    GET: /api/reseñas/pelicula/{pelicula_slug}/
    """
    serializer_class = ReseñaSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha_creacion', 'calificacion']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        pelicula_slug = self.kwargs['pelicula_slug']
        return Reseña.objects.filter(
            pelicula__slug=pelicula_slug, 
            activa=True
        ).select_related('usuario', 'pelicula')


class ReseñasPorUsuarioAPIView(generics.ListAPIView):
    """
    Lista reseñas de un usuario específico
    GET: /api/reseñas/usuario/{username}/
    """
    serializer_class = ReseñaSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['fecha_creacion', 'calificacion']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Reseña.objects.filter(
            usuario__username=username, 
            activa=True
        ).select_related('usuario', 'pelicula')


# ============ APIS DE CATEGORÍAS ============

class CategoriaListAPIView(generics.ListAPIView):
    """
    Lista todas las categorías
    GET: /api/categorias/
    """
    queryset = Categoria.objects.all().order_by('nombre')
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ============ APIS DE ESTADÍSTICAS ============

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def estadisticas_peliculas(request):
    """
    Estadísticas generales de películas
    GET: /api/estadisticas/peliculas/
    """
    peliculas_activas = Pelicula.objects.filter(activa=True)
    
    # Estadísticas básicas
    total_peliculas = peliculas_activas.count()
    promedio_calificaciones = peliculas_activas.aggregate(
        promedio=Avg('calificacion_promedio')
    )['promedio'] or 0
    
    # Películas por categoría
    peliculas_por_categoria = {}
    for categoria in Categoria.objects.all():
        count = peliculas_activas.filter(categorias=categoria).count()
        if count > 0:
            peliculas_por_categoria[categoria.nombre] = count
    
    # Película mejor calificada
    pelicula_mejor_calificada = peliculas_activas.filter(
        total_calificaciones__gt=0
    ).order_by('-calificacion_promedio').first()
    
    # Películas recientes (últimas 5)
    peliculas_recientes = peliculas_activas.order_by('-fecha_agregada')[:5]
    
    data = {
        'total_peliculas': total_peliculas,
        'peliculas_por_categoria': peliculas_por_categoria,
        'promedio_calificaciones': round(promedio_calificaciones, 2),
        'pelicula_mejor_calificada': PeliculaListSerializer(pelicula_mejor_calificada).data if pelicula_mejor_calificada else None,
        'peliculas_recientes': PeliculaListSerializer(peliculas_recientes, many=True).data
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_usuario(request):
    """
    Estadísticas del usuario autenticado
    GET: /api/estadisticas/usuario/
    """
    usuario = request.user
    
    # Estadísticas de reseñas
    reseñas_usuario = Reseña.objects.filter(usuario=usuario, activa=True)
    total_reseñas = reseñas_usuario.count()
    promedio_calificaciones_dadas = reseñas_usuario.aggregate(
        promedio=Avg('calificacion')
    )['promedio'] or 0
    
    # Películas favoritas
    peliculas_favoritas_count = 0
    comentarios_count = 0
    
    if hasattr(usuario, 'perfil'):
        peliculas_favoritas_count = usuario.perfil.peliculas_favoritas.count()
    
    # Comentarios
    comentarios_count = ComentarioPelicula.objects.filter(
        usuario=usuario, activo=True
    ).count()
    
    data = {
        'total_reseñas': total_reseñas,
        'promedio_calificaciones_dadas': round(promedio_calificaciones_dadas, 2),
        'peliculas_favoritas_count': peliculas_favoritas_count,
        'comentarios_count': comentarios_count
    }
    
    return Response(data)


# ============ APIS DE BÚSQUEDA ============

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def buscar_peliculas(request):
    """
    Búsqueda avanzada de películas
    GET: /api/buscar/?q=termino&categoria=slug&año=2020&minimo_rating=4
    """
    query = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    año = request.GET.get('año', '')
    minimo_rating = request.GET.get('minimo_rating', '')
    
    queryset = Pelicula.objects.filter(activa=True)
    
    # Filtro por término de búsqueda
    if query:
        queryset = queryset.filter(
            Q(titulo__icontains=query) |
            Q(director__icontains=query) |
            Q(reparto__icontains=query) |
            Q(sinopsis__icontains=query)
        )
    
    # Filtro por categoría
    if categoria:
        queryset = queryset.filter(categorias__slug=categoria)
    
    # Filtro por año
    if año:
        try:
            año_int = int(año)
            queryset = queryset.filter(año=año_int)
        except ValueError:
            pass
    
    # Filtro por rating mínimo
    if minimo_rating:
        try:
            rating_float = float(minimo_rating)
            queryset = queryset.filter(calificacion_promedio__gte=rating_float)
        except ValueError:
            pass
    
    # Paginación
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(queryset.distinct(), request)
    
    if page is not None:
        serializer = PeliculaListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = PeliculaListSerializer(queryset.distinct(), many=True)
    return Response(serializer.data)


# ============ APIS DE SERVICIOS EXTERNOS ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden buscar portadas
def buscar_portadas_tmdb(request):
    """
    Buscar portadas de películas en TMDB
    GET: /api/tmdb/buscar-portadas/?titulo=nombre&año=2020
    """
    titulo = request.GET.get('titulo', '').strip()
    año = request.GET.get('año', '')
    
    if not titulo:
        return Response(
            {'error': 'El parámetro "titulo" es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convertir año a entero si se proporciona
    year_int = None
    if año:
        try:
            year_int = int(año)
        except ValueError:
            return Response(
                {'error': 'El parámetro "año" debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    try:
        # Buscar en TMDB
        resultados = tmdb_service.search_movies(titulo, year_int)
        
        return Response({
            'titulo_buscado': titulo,
            'año_filtro': year_int,
            'total_resultados': len(resultados),
            'resultados': resultados
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error al consultar TMDB: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asignar_portada_tmdb(request):
    """
    Asignar portada de TMDB a una película existente
    POST: /api/tmdb/asignar-portada/
    Body: {
        "pelicula_id": 123,
        "tmdb_poster_path": "/path/to/poster.jpg",
        "tmdb_id": 456
    }
    """
    pelicula_id = request.data.get('pelicula_id')
    tmdb_poster_path = request.data.get('tmdb_poster_path')
    tmdb_id = request.data.get('tmdb_id')
    
    if not pelicula_id or not tmdb_poster_path:
        return Response(
            {'error': 'Los campos "pelicula_id" y "tmdb_poster_path" son requeridos'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Obtener la película
        pelicula = Pelicula.objects.get(id=pelicula_id, activa=True)
        
        # Verificar permisos (solo staff puede modificar)
        if not request.user.is_staff:
            return Response(
                {'error': 'Solo el staff puede asignar portadas'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generar URL completa de la portada
        from .services import get_poster_url
        poster_url_medium = get_poster_url(tmdb_poster_path, 'medium')
        poster_url_large = get_poster_url(tmdb_poster_path, 'large')
        
        # Guardar información TMDB en la película (podrías agregar campos al modelo)
        # Por ahora, solo devolvemos la información para uso manual
        
        return Response({
            'mensaje': 'Portada encontrada exitosamente',
            'pelicula': {
                'id': pelicula.id,
                'titulo': pelicula.titulo,
            },
            'tmdb_info': {
                'tmdb_id': tmdb_id,
                'poster_path': tmdb_poster_path,
                'poster_url_medium': poster_url_medium,
                'poster_url_large': poster_url_large,
            },
            'instrucciones': 'Copia la URL de la portada y úsala para actualizar el campo poster de la película'
        })
        
    except Pelicula.DoesNotExist:
        return Response(
            {'error': 'Película no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error al procesar la solicitud: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def peliculas_populares_tmdb(request):
    """
    Obtener películas populares de TMDB (para descubrimiento)
    GET: /api/tmdb/populares/
    """
    page = request.GET.get('page', 1)
    
    try:
        page_int = int(page)
        if page_int < 1:
            page_int = 1
    except ValueError:
        page_int = 1
    
    try:
        peliculas_populares = tmdb_service.get_popular_movies(page_int)
        
        return Response({
            'page': page_int,
            'total_resultados': len(peliculas_populares),
            'peliculas': peliculas_populares,
            'info': 'Películas populares obtenidas de TMDB - puedes usar estas como referencia para agregar a tu catálogo'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error al obtener películas populares: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============ APIS DE YOUTUBE TRAILERS ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_trailers_youtube(request):
    """
    Buscar trailers de películas en YouTube
    GET: /api/youtube/buscar-trailers/?movie_title=inception&year=2010
    """
    movie_title = request.GET.get('movie_title', '').strip()
    year = request.GET.get('year', '')
    
    if not movie_title:
        return Response(
            {'error': 'El parámetro "movie_title" es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Convertir año a entero si se proporciona
    year_int = None
    if year:
        try:
            year_int = int(year)
        except ValueError:
            return Response(
                {'error': 'El parámetro "year" debe ser un número válido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    try:
        # Buscar trailers en YouTube
        trailers = youtube_service.search_movie_trailer(movie_title, year_int)
        
        return Response({
            'movie_title': movie_title,
            'year': year_int,
            'total_resultados': len(trailers),
            'trailers': trailers
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error al consultar YouTube API: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_detalles_trailer(request):
    """
    Obtener detalles completos de un trailer específico
    GET: /api/youtube/trailer/{youtube_id}/
    """
    youtube_id = request.GET.get('youtube_id', '').strip()
    
    if not youtube_id:
        return Response(
            {'error': 'El parámetro "youtube_id" es requerido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Obtener detalles del trailer
        detalles = youtube_service.get_video_details(youtube_id)
        
        if detalles:
            return Response({
                'youtube_id': youtube_id,
                'detalles': detalles
            })
        else:
            return Response(
                {'error': 'Trailer no encontrado o no disponible'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error al obtener detalles del trailer: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def trailers_pelicula(request, pelicula_id):
    """
    Obtener información de trailer de una película específica
    GET: /api/peliculas/{id}/trailer/
    """
    try:
        pelicula = Pelicula.objects.get(id=pelicula_id, activa=True)
        
        if pelicula.trailer_youtube_id:
            # Obtener detalles completos del trailer
            detalles_trailer = youtube_service.get_video_details(pelicula.trailer_youtube_id)
            
            trailer_info = {
                'pelicula': {
                    'id': pelicula.id,
                    'titulo': pelicula.titulo,
                    'año': pelicula.año,
                },
                'trailer': {
                    'youtube_id': pelicula.trailer_youtube_id,
                    'embed_url': pelicula.get_trailer_embed_url(),
                    'watch_url': pelicula.get_trailer_watch_url(),
                    'detalles': detalles_trailer
                }
            }
            
            return Response(trailer_info)
        else:
            return Response({
                'pelicula': {
                    'id': pelicula.id,
                    'titulo': pelicula.titulo,
                    'año': pelicula.año,
                },
                'trailer': None,
                'message': 'Esta película no tiene trailer disponible'
            })
        
    except Pelicula.DoesNotExist:
        return Response(
            {'error': 'Película no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error al procesar la solicitud: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )