from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Categoria(models.Model):
    """Modelo para las categorías de películas"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('categoria_detalle', kwargs={'slug': self.slug})


class Pelicula(models.Model):
    """Modelo para las películas"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    año = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    director = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='peliculas'
    )
    imagen = models.ImageField(
        upload_to='peliculas/', 
        blank=True, 
        null=True,
        help_text="Imagen/poster de la película"
    )
    trailer_url = models.URLField(blank=True, help_text="URL del trailer (YouTube, etc.)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_creacion', 'titulo']
        unique_together = ['titulo', 'año']
    
    def __str__(self):
        return f"{self.titulo} ({self.año})"
    
    def get_absolute_url(self):
        return reverse('pelicula_detalle', kwargs={'pk': self.pk})
    
    def rating_promedio(self):
        """Calcula el rating promedio de las reseñas"""
        reseñas = self.reseñas.all()
        if reseñas:
            return sum([r.rating for r in reseñas]) / len(reseñas)
        return 0
    
    def total_reseñas(self):
        """Retorna el número total de reseñas"""
        return self.reseñas.count()


class PerfilUsuario(models.Model):
    """Perfil extendido para los usuarios"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='avatares/', 
        blank=True, 
        null=True,
        help_text="Foto de perfil del usuario"
    )
    categorias_favoritas = models.ManyToManyField(
        Categoria, 
        blank=True, 
        related_name='usuarios_que_prefieren'
    )
    peliculas_favoritas = models.ManyToManyField(
        Pelicula, 
        blank=True, 
        related_name='usuarios_que_favorecen'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('perfil_usuario', kwargs={'username': self.user.username})


class Reseña(models.Model):
    """Modelo para las reseñas de películas"""
    RATING_CHOICES = [
        (1, '1 - Muy Mala'),
        (2, '2 - Mala'),
        (3, '3 - Regular'),
        (4, '4 - Buena'),
        (5, '5 - Excelente'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reseñas')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='reseñas')
    rating = models.IntegerField(choices=RATING_CHOICES)
    titulo = models.CharField(max_length=200)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha_creacion']
        unique_together = ['usuario', 'pelicula']  # Un usuario solo puede reseñar una película una vez
    
    def __str__(self):
        return f"{self.titulo} - {self.pelicula.titulo} por {self.usuario.username}"
    
    def get_absolute_url(self):
        return reverse('reseña_detalle', kwargs={'pk': self.pk})
