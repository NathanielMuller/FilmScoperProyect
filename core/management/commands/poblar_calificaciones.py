from django.core.management.base import BaseCommand
from core.models import Pelicula

class Command(BaseCommand):
    help = 'Poblar calificaciones oficiales para las películas existentes'
    
    def handle(self, *args, **options):
        # Diccionario con calificaciones oficiales realistas (IMDb style, sobre 10)
        calificaciones_oficiales = {
            'Encanto': 7.2,
            'Spider-Man: No Way Home': 8.4,
            'Dune': 8.0,
            'El Conjuro': 7.5,
            'Pesadilla en Elm Street': 7.4,
            'Mad Max: Fury Road': 8.1,
            'El Caballero Oscuro': 9.0,
            'Gladiador': 8.5,
            'Vengadores: Endgame': 8.4,
            '007: Skyfall': 7.8,
            'Supercool': 6.9,
            'Chicas Malas': 7.0,
            'Zoolander': 6.5,
            'Donde Estan las Rubias': 5.8,
            'El Gran Hotel Budapest': 8.1,
            'La La Land': 8.0,
            'Eterno Resplandor de una Mente sin Recuerdos': 8.3,
            'Cuestion de Tiempo': 7.8,
            'El Diario de una Pasion': 7.8,
            'Titanic': 7.8,
            'Free Solo': 8.1,
            'Mi Maestro el Pulpo': 8.2,
            'El Viaje del Pinguino': 7.5,
            'Fahrenheit 9/11': 7.5,
            'El Dilema de las Redes': 7.6,
            'It Follows': 6.8,
            'El Exorcista': 8.1,
            'Hereditary': 7.3,
            'Midsommar': 7.1
        }
        
        peliculas_actualizadas = 0
        
        for pelicula in Pelicula.objects.all():
            calificacion = calificaciones_oficiales.get(pelicula.titulo)
            if calificacion:
                pelicula.calificacion_oficial = calificacion
                pelicula.save(update_fields=['calificacion_oficial'])
                peliculas_actualizadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {pelicula.titulo}: {calificacion}/10')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- {pelicula.titulo}: Sin calificación oficial')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n¡Proceso completado! {peliculas_actualizadas} películas actualizadas con calificaciones oficiales.')
        )