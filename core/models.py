from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Modelo de Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

# Modelo de Película
class Pelicula(models.Model):
    # Información básica
    titulo = models.CharField(max_length=200)
    titulo_original = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    
    # Detalles
    año = models.PositiveIntegerField()
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    director = models.CharField(max_length=200)
    reparto = models.TextField(help_text="Actores principales separados por comas")
    sinopsis = models.TextField()
    
    # Categorías (una película puede tener múltiples géneros)
    categorias = models.ManyToManyField(Categoria, related_name='peliculas')
    
    # Imágenes y multimedia
    poster = models.URLField(blank=True, help_text="URL del poster desde TMDB")
    banner = models.ImageField(upload_to='peliculas/banners/', blank=True)
    trailer_youtube_id = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="ID del trailer oficial en YouTube (ej: dQw4w9WgXcQ)"
    )
    
    # Metadatos
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    fecha_actualizada = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    # Calificación oficial (estática, de fuentes externas como IMDb)
    calificacion_oficial = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Calificación oficial de fuentes externas (TMDB, IMDb, Rotten Tomatoes, etc.)"
    )
    
    # Calificación FilmScoper (promedio de usuarios)
    calificacion_promedio = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Promedio de calificaciones de usuarios de FilmScoper"
    )
    total_calificaciones = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_agregada']
    
    def __str__(self):
        return f"{self.titulo} ({self.año})"
    
    def get_absolute_url(self):
        return reverse('core:pelicula', kwargs={'slug': self.slug})
    
    def actualizar_calificacion(self):
        """Actualiza la calificación promedio basada en las reseñas"""
        reseñas = self.reseñas.filter(activa=True)
        if reseñas.exists():
            self.calificacion_promedio = reseñas.aggregate(
                promedio=models.Avg('calificacion')
            )['promedio']
            self.total_calificaciones = reseñas.count()
        else:
            self.calificacion_promedio = 0.0
            self.total_calificaciones = 0
        self.save(update_fields=['calificacion_promedio', 'total_calificaciones'])
    
    def get_calificacion_oficial_display(self):
        """Devuelve la calificación oficial formateada (sobre 10)"""
        if self.calificacion_oficial > 0:
            return f"{self.calificacion_oficial:.1f}/10"
        return "N/A"
    
    def get_calificacion_filmscoper_display(self):
        """Devuelve la calificación de FilmScoper formateada (sobre 5)"""
        if self.calificacion_promedio > 0:
            return f"{self.calificacion_promedio:.1f}/5"
        return "Sin calificar"
    
    def get_poster_url(self):
        """Devuelve la URL del poster desde TMDB"""
        return self.poster if self.poster else None
    
    def get_estrellas_oficial(self):
        """Convierte la calificación oficial (1-10) a estrellas (1-5)"""
        if self.calificacion_oficial > 0:
            return round((self.calificacion_oficial / 10) * 5, 1)
        return 0
    
    def get_estrellas_filmscoper(self):
        """Devuelve las estrellas de FilmScoper directamente"""
        return float(self.calificacion_promedio) if self.calificacion_promedio > 0 else 0
    
    def get_trailer_embed_url(self):
        """Devuelve la URL de embed para YouTube si hay trailer disponible"""
        if self.trailer_youtube_id:
            return f"https://www.youtube.com/embed/{self.trailer_youtube_id}"
        return None
    
    def get_trailer_watch_url(self):
        """Devuelve la URL directa de YouTube para ver el trailer"""
        if self.trailer_youtube_id:
            return f"https://www.youtube.com/watch?v={self.trailer_youtube_id}"
        return None
    
    def has_trailer(self):
        """Verifica si la película tiene un trailer disponible"""
        return bool(self.trailer_youtube_id)

# Perfil extendido del usuario
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', blank=True)
    biografia = models.TextField(max_length=500, blank=True)
    
    # Géneros favoritos
    generos_favoritos = models.ManyToManyField(Categoria, blank=True, related_name='usuarios_favoritos')
    
    # Películas favoritas y para ver más tarde
    peliculas_favoritas = models.ManyToManyField(Pelicula, blank=True, related_name='usuarios_favoritas')
    ver_mas_tarde = models.ManyToManyField(Pelicula, blank=True, related_name='usuarios_ver_mas_tarde')
    
    # Configuraciones
    recibir_notificaciones = models.BooleanField(default=True)
    perfil_publico = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

# Modelo de Reseña/Calificación
class Reseña(models.Model):
    # Relaciones
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reseñas')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='reseñas')
    
    # Calificación (1-5 estrellas)
    calificacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    
    # Comentario (opcional)
    comentario = models.TextField(blank=True, max_length=1000)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        unique_together = ('usuario', 'pelicula')  # Un usuario solo puede reseñar una película una vez
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo} ({self.calificacion}⭐)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar calificación promedio de la película
        self.pelicula.actualizar_calificacion()

# Lista de Favoritos
class ListaFavoritos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='en_favoritos')
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Película Favorita"
        verbose_name_plural = "Películas Favoritas"
        unique_together = ('usuario', 'pelicula')
        ordering = ['-fecha_agregada']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"

# Lista de "Ver más tarde"
class ListaVerMasTarde(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ver_mas_tarde')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='en_ver_mas_tarde')
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ver Más Tarde"
        verbose_name_plural = "Ver Más Tarde"
        unique_together = ('usuario', 'pelicula')
        ordering = ['-fecha_agregada']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"


# ===== MODELOS PARA SISTEMA DE FOROS =====

class ForoCategoria(models.Model):
    """Foros organizados por categorías de películas"""
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE, related_name='foro')
    descripcion = models.TextField(blank=True, help_text="Descripción del foro de esta categoría")
    
    # Configuraciones
    activo = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Foro de Categoría"
        verbose_name_plural = "Foros de Categorías"
        ordering = ['categoria__nombre']
    
    def __str__(self):
        return f"Foro de {self.categoria.nombre}"
    
    @property
    def total_temas(self):
        return self.temas.filter(activo=True).count()
    
    @property
    def ultimo_tema(self):
        return self.temas.filter(activo=True).order_by('-fecha_creacion').first()


class TemaDeForo(models.Model):
    """Temas de discusión dentro de cada foro"""
    foro = models.ForeignKey(ForoCategoria, on_delete=models.CASCADE, related_name='temas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temas_creados')
    
    # Contenido
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    
    # Opcionales: relacionar con película específica
    pelicula_relacionada = models.ForeignKey(
        Pelicula, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='temas_foro',
        help_text="Película específica de la que trata este tema (opcional)"
    )
    
    # Estado
    activo = models.BooleanField(default=True)
    cerrado = models.BooleanField(default=False, help_text="Si está cerrado, no se pueden agregar respuestas")
    destacado = models.BooleanField(default=False, help_text="Temas destacados aparecen primero")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tema de Foro"
        verbose_name_plural = "Temas de Foro"
        ordering = ['-destacado', '-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.foro.categoria.nombre}"
    
    @property
    def total_respuestas(self):
        return self.respuestas.filter(activo=True).count()
    
    @property
    def ultima_respuesta(self):
        return self.respuestas.filter(activo=True).order_by('-fecha_creacion').first()
    
    def save(self, *args, **kwargs):
        # Actualizar fecha de última actividad del tema
        from django.utils import timezone
        self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)


class RespuestaForo(models.Model):
    """Respuestas a los temas del foro"""
    tema = models.ForeignKey(TemaDeForo, on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas_foro')
    
    # Contenido
    contenido = models.TextField()
    
    # Estado
    activo = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Respuesta de Foro"
        verbose_name_plural = "Respuestas de Foro"
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f"Respuesta de {self.autor.username} en '{self.tema.titulo}'"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar la fecha de última actividad del tema
        self.tema.save()


# ===== MODELO PARA COMENTARIOS MÚLTIPLES =====

class ComentarioPelicula(models.Model):
    """Comentarios múltiples por usuario en películas (separado de calificaciones)"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_peliculas')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='comentarios')
    
    # Contenido del comentario
    contenido = models.TextField(max_length=1000, help_text="Comparte tu opinión sobre esta película")
    
    # Respuesta a otro comentario (para threading)
    respuesta_a = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='respuestas',
        help_text="Comentario al que responde (opcional)"
    )
    
    # Estado
    activo = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentario de Película"
        verbose_name_plural = "Comentarios de Películas"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['pelicula', '-fecha_creacion']),
            models.Index(fields=['usuario', '-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo} - {self.fecha_creacion.strftime('%d/%m/%Y')}"
    
    @property
    def es_respuesta(self):
        """Indica si este comentario es una respuesta a otro"""
        return self.respuesta_a is not None
    
    @property
    def total_respuestas(self):
        """Número de respuestas que tiene este comentario"""
        return self.respuestas.filter(activo=True).count()
