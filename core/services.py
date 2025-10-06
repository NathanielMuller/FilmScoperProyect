import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class TMDBService:
    """
    Servicio para interactuar con The Movie Database (TMDB) API
    Funcionalidades:
    - Búsqueda de películas por título
    - Obtención de URLs de portadas
    - Cache de resultados para optimizar rendimiento
    """
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
    
    # Tamaños de imágenes disponibles en TMDB
    POSTER_SIZES = {
        'small': 'w185',      # 185px de ancho
        'medium': 'w342',     # 342px de ancho  
        'large': 'w500',      # 500px de ancho
        'xlarge': 'w780',     # 780px de ancho
        'original': 'original' # Tamaño original
    }
    
    def __init__(self):
        """Inicializar el servicio con la API key"""
        self.api_key = getattr(settings, 'TMDB_API_KEY', None)
        if not self.api_key:
            logger.warning("TMDB_API_KEY no configurada en settings")
    
    def _make_request(self, endpoint, params=None):
        """
        Realizar petición HTTP a la API de TMDB
        
        Args:
            endpoint (str): Endpoint de la API (ej: '/search/movie')
            params (dict): Parámetros adicionales para la consulta
            
        Returns:
            dict: Respuesta JSON de la API o None si hay error
        """
        if not self.api_key:
            logger.error("No se puede hacer petición sin API key")
            return None
        
        # Preparar parámetros base
        request_params = {
            'api_key': self.api_key,
            'language': 'es-ES',  # Obtener resultados en español
        }
        
        # Agregar parámetros adicionales
        if params:
            request_params.update(params)
        
        try:
            url = f"{self.BASE_URL}{endpoint}"
            logger.info(f"Realizando petición a TMDB: {url}")
            
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar TMDB API: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Error al decodificar JSON de TMDB: {str(e)}")
            return None
    
    def search_movies(self, title, year=None, limit=5):
        """
        Buscar películas por título en TMDB
        
        Args:
            title (str): Título de la película a buscar
            year (int, optional): Año de la película para filtrar resultados
            limit (int): Número máximo de resultados (default: 5)
            
        Returns:
            list: Lista de películas encontradas con información básica
        """
        if not title or not title.strip():
            return []
        
        # Crear clave de cache única
        cache_key = f"tmdb_search_{title.lower().replace(' ', '_')}_{year or 'any'}"
        
        # Intentar obtener desde cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Resultados obtenidos desde cache: {title}")
            return cached_result[:limit]
        
        # Preparar parámetros de búsqueda
        params = {
            'query': title.strip(),
            'page': 1,
        }
        
        # Agregar filtro por año si se proporciona
        if year:
            params['year'] = year
        
        # Realizar petición
        data = self._make_request('/search/movie', params)
        
        if not data or 'results' not in data:
            return []
        
        # Procesar resultados
        movies = []
        for movie_data in data['results'][:limit]:
            movie_info = self._process_movie_data(movie_data)
            if movie_info:
                movies.append(movie_info)
        
        # Guardar en cache por 1 hora
        cache.set(cache_key, movies, 3600)
        
        logger.info(f"Encontradas {len(movies)} películas para '{title}'")
        return movies
    
    def _process_movie_data(self, movie_data):
        """
        Procesar datos de película desde TMDB API
        
        Args:
            movie_data (dict): Datos raw de la película desde TMDB
            
        Returns:
            dict: Información procesada de la película
        """
        if not movie_data:
            return None
        
        return {
            'tmdb_id': movie_data.get('id'),
            'title': movie_data.get('title', ''),
            'original_title': movie_data.get('original_title', ''),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', ''),
            'year': movie_data.get('release_date', '')[:4] if movie_data.get('release_date') else None,
            'vote_average': movie_data.get('vote_average', 0),
            'vote_count': movie_data.get('vote_count', 0),
            'popularity': movie_data.get('popularity', 0),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'poster_urls': self._get_poster_urls(movie_data.get('poster_path')),
            'backdrop_urls': self._get_poster_urls(movie_data.get('backdrop_path')),
        }
    
    def _get_poster_urls(self, image_path):
        """
        Generar URLs completas para las imágenes en diferentes tamaños
        
        Args:
            image_path (str): Ruta de la imagen desde TMDB (ej: '/abc123.jpg')
            
        Returns:
            dict: URLs de la imagen en diferentes tamaños
        """
        if not image_path:
            return {}
        
        urls = {}
        for size_name, size_code in self.POSTER_SIZES.items():
            urls[size_name] = f"{self.IMAGE_BASE_URL}/{size_code}{image_path}"
        
        return urls
    
    def get_movie_details(self, tmdb_id):
        """
        Obtener detalles completos de una película por su ID de TMDB
        
        Args:
            tmdb_id (int): ID de la película en TMDB
            
        Returns:
            dict: Detalles completos de la película
        """
        if not tmdb_id:
            return None
        
        cache_key = f"tmdb_movie_details_{tmdb_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        # Obtener detalles básicos
        movie_data = self._make_request(f'/movie/{tmdb_id}')
        if not movie_data:
            return None
        
        # Obtener créditos (director y reparto)
        credits_data = self._make_request(f'/movie/{tmdb_id}/credits')
        
        # Procesar datos completos
        movie_details = self._process_complete_movie_data(movie_data, credits_data)
        
        # Guardar en cache por 24 horas
        cache.set(cache_key, movie_details, 86400)
        return movie_details
    
    def _process_complete_movie_data(self, movie_data, credits_data=None):
        """
        Procesar datos completos de película desde TMDB API incluyendo créditos
        
        Args:
            movie_data (dict): Datos básicos de la película
            credits_data (dict): Datos de créditos (cast & crew)
            
        Returns:
            dict: Información completa procesada de la película
        """
        if not movie_data:
            return None
        
        # Procesar géneros
        genres = []
        if movie_data.get('genres'):
            genres = [genre['name'] for genre in movie_data['genres']]
        
        # Procesar director (del crew)
        director = ""
        if credits_data and credits_data.get('crew'):
            for crew_member in credits_data['crew']:
                if crew_member.get('job') == 'Director':
                    director = crew_member.get('name', '')
                    break
        
        # Procesar reparto principal (primeros 10)
        cast_list = []
        if credits_data and credits_data.get('cast'):
            cast_list = [
                actor.get('name', '') 
                for actor in credits_data['cast'][:10] 
                if actor.get('name')
            ]
        
        # Construir datos completos
        complete_data = {
            'tmdb_id': movie_data.get('id'),
            'title': movie_data.get('title', ''),
            'original_title': movie_data.get('original_title', ''),
            'overview': movie_data.get('overview', ''),
            'release_date': movie_data.get('release_date', ''),
            'year': movie_data.get('release_date', '')[:4] if movie_data.get('release_date') else None,
            'runtime': movie_data.get('runtime', 0),  # Duración en minutos
            'vote_average': movie_data.get('vote_average', 0),
            'vote_count': movie_data.get('vote_count', 0),
            'popularity': movie_data.get('popularity', 0),
            'poster_path': movie_data.get('poster_path'),
            'backdrop_path': movie_data.get('backdrop_path'),
            'poster_urls': self._get_poster_urls(movie_data.get('poster_path')),
            'backdrop_urls': self._get_poster_urls(movie_data.get('backdrop_path')),
            
            # Datos adicionales procesados
            'genres': genres,
            'genres_string': ', '.join(genres),  # Para mostrar en texto
            'director': director,
            'cast': cast_list,
            'cast_string': ', '.join(cast_list),  # Para mostrar en texto
            'budget': movie_data.get('budget', 0),
            'revenue': movie_data.get('revenue', 0),
            'status': movie_data.get('status', ''),
            'tagline': movie_data.get('tagline', ''),
            
            # URLs completas para usar directamente
            'poster_url_medium': self._get_poster_urls(movie_data.get('poster_path')).get('medium', ''),
            'poster_url_large': self._get_poster_urls(movie_data.get('poster_path')).get('large', ''),
            'backdrop_url_large': self._get_poster_urls(movie_data.get('backdrop_path')).get('large', ''),
        }
        
        return complete_data
    
    def get_popular_movies(self, page=1):
        """
        Obtener películas populares de TMDB
        
        Args:
            page (int): Página de resultados (default: 1)
            
        Returns:
            list: Lista de películas populares
        """
        params = {'page': page}
        data = self._make_request('/movie/popular', params)
        
        if not data or 'results' not in data:
            return []
        
        movies = []
        for movie_data in data['results']:
            movie_info = self._process_movie_data(movie_data)
            if movie_info:
                movies.append(movie_info)
        
        return movies


# Instancia global del servicio para uso en views
tmdb_service = TMDBService()


def search_movie_posters(title, year=None):
    """
    Función helper para buscar portadas de películas
    
    Args:
        title (str): Título de la película
        year (int, optional): Año de la película
        
    Returns:
        list: Lista de resultados con URLs de portadas
    """
    return tmdb_service.search_movies(title, year)


def get_poster_url(poster_path, size='medium'):
    """
    Función helper para generar URL de poster
    
    Args:
        poster_path (str): Ruta del poster desde TMDB
        size (str): Tamaño deseado ('small', 'medium', 'large', 'xlarge', 'original')
        
    Returns:
        str: URL completa del poster
    """
    if not poster_path:
        return None
    
    size_code = TMDBService.POSTER_SIZES.get(size, 'w342')
    return f"{TMDBService.IMAGE_BASE_URL}/{size_code}{poster_path}"