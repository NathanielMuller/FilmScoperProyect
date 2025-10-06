from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Categoria, Pelicula, PerfilUsuario, Reseña, ListaFavoritos, ListaVerMasTarde

# Configuración del admin para Categoría
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'descripcion', 'get_peliculas_count']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']
    readonly_fields = ['get_peliculas_count']
    
    def get_peliculas_count(self, obj):
        return obj.peliculas.count()
    get_peliculas_count.short_description = 'N° Películas'

# Configuración del admin para Película
@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'año', 'director', 'get_poster_preview', 'calificacion_promedio', 'total_calificaciones', 'activa']
    list_filter = ['año', 'categorias', 'activa', 'fecha_agregada']
    search_fields = ['titulo', 'titulo_original', 'director', 'reparto']
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ['categorias']
    list_editable = ['activa']
    
    # Medios personalizados para incluir CSS y JS
    class Media:
        css = {
            'all': ('admin/css/tmdb_integration.css',)
        }
        js = ('admin/js/tmdb_integration.js',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'titulo_original', 'slug', 'año', 'duracion')
        }),
        ('Detalles', {
            'fields': ('director', 'reparto', 'sinopsis', 'categorias', 'calificacion_oficial')
        }),
        ('Imágenes', {
            'fields': ('poster', 'banner')
        }),

        ('Configuración', {
            'fields': ('activa',)
        }),
        ('Estadísticas', {
            'fields': ('calificacion_promedio', 'total_calificaciones'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['calificacion_promedio', 'total_calificaciones']
    
    def get_poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="50" height="75" style="border-radius: 4px;" />', obj.poster)
        return "Sin poster"
    get_poster_preview.short_description = 'Poster'

# Inline para Perfil de Usuario
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ('bio', 'avatar', 'fecha_nacimiento')

# Configuración personalizada para el modelo User
class UsuarioAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_reseñas_count', 'date_joined')
    
    def get_reseñas_count(self, obj):
        return Reseña.objects.filter(usuario=obj).count()
    get_reseñas_count.short_description = 'Reseñas'

# Re-registrar User con la configuración personalizada
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

# Configuración del admin para Reseña
@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pelicula', 'calificacion', 'get_comentario_preview', 'fecha_creacion', 'activa']
    list_filter = ['calificacion', 'activa', 'fecha_creacion']
    search_fields = ['usuario__username', 'pelicula__titulo', 'comentario']
    raw_id_fields = ['usuario', 'pelicula']
    list_editable = ['activa']
    
    fieldsets = (
        ('Reseña', {
            'fields': ('usuario', 'pelicula', 'calificacion', 'comentario')
        }),
        ('Configuración', {
            'fields': ('activa',)
        })
    )
    
    def get_comentario_preview(self, obj):
        if obj.comentario:
            return obj.comentario[:50] + '...' if len(obj.comentario) > 50 else obj.comentario
        return "Sin comentario"
    get_comentario_preview.short_description = 'Comentario'

# Configuración del admin para Lista de Favoritos
@admin.register(ListaFavoritos)
class ListaFavoritosAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pelicula', 'fecha_agregada']
    list_filter = ['fecha_agregada']
    search_fields = ['usuario__username', 'pelicula__titulo']
    raw_id_fields = ['usuario', 'pelicula']

# Configuración del admin para Ver Más Tarde
@admin.register(ListaVerMasTarde)
class ListaVerMasTardeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'pelicula', 'fecha_agregada']
    list_filter = ['fecha_agregada']
    search_fields = ['usuario__username', 'pelicula__titulo']
    raw_id_fields = ['usuario', 'pelicula']

# Personalizar el título del admin
admin.site.site_header = "🎬 FilmScoper - Panel de Administración"
admin.site.site_title = "FilmScoper Admin"
admin.site.index_title = "Gestión de Contenido y Usuarios"
