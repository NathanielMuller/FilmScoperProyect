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


class YouTubeService:
    """
    Servicio para interactuar con YouTube Data API v3
    Funcionalidades:
    - Búsqueda de trailers oficiales por título de película
    - Obtención de metadatos de videos
    - Cache de resultados para optimizar rendimiento
    """
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        """Inicializar el servicio con la API key"""
        self.api_key = getattr(settings, 'YOUTUBE_API_KEY', None)
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY no configurada en settings")
    
    def _make_request(self, endpoint, params=None):
        """
        Realizar petición HTTP a la API de YouTube
        
        Args:
            endpoint (str): Endpoint de la API (ej: '/search')
            params (dict): Parámetros adicionales para la consulta
            
        Returns:
            dict: Respuesta JSON de la API o None si hay error
        """
        if not self.api_key:
            logger.error("No se puede hacer petición sin YouTube API key")
            return None
        
        # Preparar parámetros base
        request_params = {
            'key': self.api_key,
        }
        
        # Agregar parámetros adicionales
        if params:
            request_params.update(params)
        
        try:
            url = f"{self.BASE_URL}{endpoint}"
            logger.info(f"Realizando petición a YouTube: {url}")
            
            response = requests.get(url, params=request_params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar YouTube API: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Error al decodificar JSON de YouTube: {str(e)}")
            return None
    
    def search_movie_trailer(self, movie_title, year=None, limit=10):
        """
        Buscar trailers de película en YouTube
        
        Args:
            movie_title (str): Título de la película
            year (int, optional): Año de la película para mejorar búsqueda
            limit (int): Número máximo de resultados (default: 10)
            
        Returns:
            list: Lista de trailers encontrados con metadatos
        """
        if not movie_title or not movie_title.strip():
            return []
        
        # Crear clave de cache
        cache_key = f"youtube_search_{movie_title.lower().replace(' ', '_')}_{year or 'any'}"
        
        # Intentar obtener desde cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Trailers obtenidos desde cache: {movie_title}")
            return cached_result[:limit]
        
        # Intentar múltiples estrategias de búsqueda
        trailers = []
        
        # Estrategia 1: Búsqueda con "official trailer"
        query1 = f"{movie_title.strip()} official trailer"
        if year:
            query1 += f" {year}"
        
        trailers.extend(self._search_with_query(query1, limit=5))
        
        # Estrategia 2: Solo "trailer" si no encontramos suficientes
        if len(trailers) < 3:
            query2 = f"{movie_title.strip()} trailer"
            if year:
                query2 += f" {year}"
            trailers.extend(self._search_with_query(query2, limit=5))
        
        # Estrategia 3: Búsqueda más amplia si aún no hay resultados
        if len(trailers) < 1:
            query3 = f"{movie_title.strip()}"
            trailers.extend(self._search_with_query(query3, limit=3, filter_trailers=False))
        
        # Eliminar duplicados y filtrar
        seen_ids = set()
        unique_trailers = []
        for trailer in trailers:
            if trailer['youtube_id'] not in seen_ids:
                seen_ids.add(trailer['youtube_id'])
                unique_trailers.append(trailer)
        
        # Guardar en cache por 24 horas
        cache.set(cache_key, unique_trailers, 86400)
        
        logger.info(f"Encontrados {len(unique_trailers)} trailers para '{movie_title}'")
        return unique_trailers[:limit]
    
    def _search_with_query(self, query, limit=5, filter_trailers=True):
        """
        Realizar búsqueda con una query específica
        """
        # Parámetros de búsqueda más flexibles
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': limit,
            'order': 'relevance',
            'safeSearch': 'moderate',  # Menos restrictivo
        }
        
        # Realizar petición
        data = self._make_request('/search', params)
        
        if not data or 'items' not in data:
            return []
        
        # Procesar resultados
        trailers = []
        for item in data['items']:
            trailer_info = self._process_video_data(item)
            if trailer_info:
                # Si filter_trailers es False, agregar todos los videos
                # Si es True, solo agregar si parece ser trailer
                if not filter_trailers or self._is_likely_trailer(trailer_info, query):
                    trailers.append(trailer_info)
        
        return trailers
    
    def _process_video_data(self, video_data):
        """
        Procesar datos de video desde YouTube API
        
        Args:
            video_data (dict): Datos raw del video desde YouTube
            
        Returns:
            dict: Información procesada del trailer
        """
        if not video_data or 'snippet' not in video_data:
            return None
        
        snippet = video_data['snippet']
        video_id = video_data['id'].get('videoId') if isinstance(video_data['id'], dict) else video_data['id']
        
        return {
            'youtube_id': video_id,
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
            'embed_url': f'https://www.youtube.com/embed/{video_id}',
            'watch_url': f'https://www.youtube.com/watch?v={video_id}',
            'channel_id': snippet.get('channelId', ''),
        }
    
    def _is_likely_trailer(self, trailer_info, search_query):
        """
        Determinar si un video es probablemente un trailer
        
        Args:
            trailer_info (dict): Información del trailer
            search_query (str): Query de búsqueda original
            
        Returns:
            bool: True si parece ser un trailer
        """
        title_lower = trailer_info['title'].lower()
        description_lower = trailer_info['description'].lower()
        
        # Palabras clave que indican trailers
        trailer_keywords = [
            'trailer', 'official trailer', 'teaser', 'preview', 
            'tráiler', 'avance', 'adelanto', 'película'
        ]
        
        # Verificar si contiene palabras clave de trailer
        has_trailer_keywords = any(keyword in title_lower for keyword in trailer_keywords)
        
        # Verificar si el título contiene parte del query de búsqueda
        query_words = search_query.lower().split()
        movie_words = [word for word in query_words if word not in ['trailer', 'official', 'tráiler']]
        has_movie_reference = any(word in title_lower for word in movie_words)
        
        # Canales oficiales comunes (studios, distribuidores)
        trusted_channels = [
            'sony pictures', 'universal pictures', 'warner bros', 'disney', 'marvel',
            'paramount pictures', '20th century', 'fox', 'lionsgate', 'netflix',
            'amazon prime', 'hbo', 'hulu', 'sony', 'warner', 'universal', 'movieclips',
            'trailers', 'entertainment', 'film', 'movie', 'cinema'
        ]
        
        channel_lower = trailer_info['channel_title'].lower()
        is_trusted_channel = any(channel in channel_lower for channel in trusted_channels)
        
        # Es probable trailer si:
        # 1. Tiene palabras clave de trailer, O
        # 2. Viene de canal confiable Y hace referencia a la película
        return has_trailer_keywords or (is_trusted_channel and has_movie_reference)
    
    def _is_likely_official_trailer(self, trailer_info, movie_title):
        """
        Determinar si un video es probablemente un trailer oficial
        
        Args:
            trailer_info (dict): Información del trailer
            movie_title (str): Título original de la película
            
        Returns:
            bool: True si parece ser un trailer oficial
        """
        title_lower = trailer_info['title'].lower()
        movie_lower = movie_title.lower()
        
        # Criterios para identificar trailers oficiales
        official_indicators = [
            'official trailer' in title_lower,
            'official' in title_lower and 'trailer' in title_lower,
            'trailer' in title_lower and any(word in movie_lower for word in title_lower.split()),
        ]
        
        # Canales oficiales comunes (studios, distributores)
        trusted_channels = [
            'sony pictures', 'universal pictures', 'warner bros', 'disney', 'marvel',
            'paramount pictures', '20th century', 'fox', 'lionsgate', 'netflix',
            'amazon prime', 'hbo', 'hulu', 'sony', 'warner', 'universal'
        ]
        
        channel_lower = trailer_info['channel_title'].lower()
        is_official_channel = any(channel in channel_lower for channel in trusted_channels)
        
        return any(official_indicators) or is_official_channel
    
    def get_video_details(self, youtube_id):
        """
        Obtener detalles específicos de un video de YouTube
        
        Args:
            youtube_id (str): ID del video en YouTube
            
        Returns:
            dict: Detalles completos del video
        """
        if not youtube_id:
            return None
        
        cache_key = f"youtube_video_{youtube_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': youtube_id
        }
        
        data = self._make_request('/videos', params)
        
        if not data or 'items' not in data or not data['items']:
            return None
        
        video_item = data['items'][0]
        details = self._process_detailed_video_data(video_item)
        
        # Guardar en cache por 24 horas
        cache.set(cache_key, details, 86400)
        return details
    
    def _process_detailed_video_data(self, video_data):
        """Procesar datos detallados de video con estadísticas"""
        snippet = video_data.get('snippet', {})
        statistics = video_data.get('statistics', {})
        content_details = video_data.get('contentDetails', {})
        
        return {
            'youtube_id': video_data.get('id'),
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'duration': content_details.get('duration', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
            'embed_url': f'https://www.youtube.com/embed/{video_data.get("id")}',
            'watch_url': f'https://www.youtube.com/watch?v={video_data.get("id")}',
        }


# Instancia global del servicio YouTube
youtube_service = YouTubeService()