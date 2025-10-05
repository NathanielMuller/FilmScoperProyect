from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pelicula, Categoria, Reseña, PerfilUsuario, ComentarioPelicula


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'slug', 'descripcion']


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer básico para el modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined']


class PeliculaListSerializer(serializers.ModelSerializer):
    """Serializer para listar películas (información básica)"""
    categorias = CategoriaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pelicula
        fields = [
            'id', 'titulo', 'titulo_original', 'slug', 'año', 
            'duracion', 'director', 'categorias', 'poster', 
            'calificacion_oficial', 'calificacion_promedio', 
            'total_calificaciones', 'fecha_agregada'
        ]


class PeliculaDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalles completos de películas"""
    categorias = CategoriaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pelicula
        fields = [
            'id', 'titulo', 'titulo_original', 'slug', 'año', 
            'duracion', 'director', 'reparto', 'sinopsis', 
            'categorias', 'poster', 'banner', 'calificacion_oficial', 
            'calificacion_promedio', 'total_calificaciones', 
            'fecha_agregada', 'fecha_actualizada'
        ]


class PeliculaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar películas"""
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), many=True
    )
    
    class Meta:
        model = Pelicula
        fields = [
            'titulo', 'titulo_original', 'slug', 'año', 
            'duracion', 'director', 'reparto', 'sinopsis', 
            'categorias', 'poster', 'banner', 'calificacion_oficial'
        ]
    
    def validate_año(self, value):
        """Validar que el año sea razonable"""
        if value < 1888 or value > 2030:  # 1888 es el año de la primera película
            raise serializers.ValidationError(
                "El año debe estar entre 1888 y 2030"
            )
        return value
    
    def validate_duracion(self, value):
        """Validar duración de la película"""
        if value < 1 or value > 600:  # Entre 1 minuto y 10 horas
            raise serializers.ValidationError(
                "La duración debe estar entre 1 y 600 minutos"
            )
        return value


class ReseñaSerializer(serializers.ModelSerializer):
    """Serializer para reseñas"""
    usuario = UsuarioSerializer(read_only=True)
    pelicula_titulo = serializers.CharField(source='pelicula.titulo', read_only=True)
    
    class Meta:
        model = Reseña
        fields = [
            'id', 'usuario', 'pelicula', 'pelicula_titulo', 
            'calificacion', 'titulo', 'comentario', 'activa',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate_calificacion(self, value):
        """Validar que la calificación esté en el rango correcto"""
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "La calificación debe estar entre 1 y 5 estrellas"
            )
        return value
    
    def create(self, validated_data):
        """Crear una nueva reseña"""
        # Asignar el usuario autenticado
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class ReseñaCreateSerializer(serializers.ModelSerializer):
    """Serializer simplificado para crear reseñas"""
    class Meta:
        model = Reseña
        fields = ['pelicula', 'calificacion', 'titulo', 'comentario']
    
    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "La calificación debe estar entre 1 y 5 estrellas"
            )
        return value
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class ComentarioPeliculaSerializer(serializers.ModelSerializer):
    """Serializer para comentarios de películas"""
    usuario = UsuarioSerializer(read_only=True)
    pelicula_titulo = serializers.CharField(source='pelicula.titulo', read_only=True)
    total_respuestas = serializers.ReadOnlyField()
    
    class Meta:
        model = ComentarioPelicula
        fields = [
            'id', 'usuario', 'pelicula', 'pelicula_titulo', 
            'contenido', 'respuesta_a', 'total_respuestas',
            'activo', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


# Serializers para estadísticas y datos agregados

class PeliculaStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas de películas"""
    total_peliculas = serializers.IntegerField()
    peliculas_por_categoria = serializers.DictField()
    promedio_calificaciones = serializers.FloatField()
    pelicula_mejor_calificada = PeliculaListSerializer()
    peliculas_recientes = PeliculaListSerializer(many=True)


class UsuarioStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas de usuarios"""
    total_reseñas = serializers.IntegerField()
    promedio_calificaciones_dadas = serializers.FloatField()
    peliculas_favoritas_count = serializers.IntegerField()
    comentarios_count = serializers.IntegerField()