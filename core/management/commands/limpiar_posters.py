from django.core.management.base import BaseCommand
from core.models import Pelicula

class Command(BaseCommand):
    help = 'Limpia los campos de poster que contienen rutas de archivos locales en lugar de URLs'

    def handle(self, *args, **options):
        # Buscar películas con rutas de archivos locales (no URLs válidas)
        peliculas_problema = []
        
        for pelicula in Pelicula.objects.all():
            # Si el poster no está vacío y no es una URL válida (no empieza con http)
            if pelicula.poster and not pelicula.poster.startswith('http'):
                peliculas_problema.append(pelicula)
                
        self.stdout.write(f"Encontradas {len(peliculas_problema)} películas con rutas de archivos locales:")
        
        for pelicula in peliculas_problema:
            self.stdout.write(f"- {pelicula.titulo}: '{pelicula.poster}'")
            
        if peliculas_problema:
            respuesta = input("\n¿Quieres limpiar estos campos (vaciarlos)? (y/N): ")
            if respuesta.lower() in ['y', 'yes', 's', 'si']:
                for pelicula in peliculas_problema:
                    pelicula.poster = ''  # Vaciar el campo
                    pelicula.save()
                    
                self.stdout.write(
                    self.style.SUCCESS(f"Se limpiaron {len(peliculas_problema)} películas.")
                )
            else:
                self.stdout.write("Operación cancelada.")
        else:
            self.stdout.write(self.style.SUCCESS("No se encontraron películas con problemas de poster."))