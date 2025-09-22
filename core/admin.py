from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Categoria, Pelicula, PerfilUsuario, Reseña


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'año', 'director', 'categoria', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'año', 'activo', 'fecha_creacion']
    search_fields = ['titulo', 'director']
    list_editable = ['activo']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'año', 'director', 'categoria')
        }),
        ('Detalles', {
            'fields': ('duracion', 'imagen', 'trailer_url')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    filter_horizontal = ['categorias_favoritas', 'peliculas_favoritas']


class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)


@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'pelicula', 'usuario', 'rating', 'fecha_creacion']
    list_filter = ['rating', 'fecha_creacion', 'pelicula__categoria']
    search_fields = ['titulo', 'pelicula__titulo', 'usuario__username']
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
