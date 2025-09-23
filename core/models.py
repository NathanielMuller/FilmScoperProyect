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
    
    # Imágenes
    poster = models.ImageField(upload_to='peliculas/posters/', blank=True)
    banner = models.ImageField(upload_to='peliculas/banners/', blank=True)
    
    # Metadatos
    fecha_agregada = models.DateTimeField(auto_now_add=True)
    fecha_actualizada = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    # Calificación promedio (se calculará automáticamente)
    calificacion_promedio = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
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
