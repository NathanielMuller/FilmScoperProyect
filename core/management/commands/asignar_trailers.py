from django.core.management.base import BaseCommand
from core.models import Pelicula
from core.services import youtube_service
import time

class Command(BaseCommand):
    help = 'Asignar trailers automáticamente a todas las películas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Número máximo de películas a procesar (default: 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Sobrescribir trailers existentes'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS(f'🎬 Asignando trailers a películas...')
        )
        
        # Obtener películas sin trailer o todas si force=True
        if force:
            peliculas = Pelicula.objects.all()[:limit]
            self.stdout.write(f"Procesando {len(peliculas)} películas (forzando actualización)")
        else:
            peliculas = Pelicula.objects.filter(
                trailer_youtube_id__isnull=True
            )[:limit]
            self.stdout.write(f"Procesando {len(peliculas)} películas sin trailer")
        
        if not peliculas:
            self.stdout.write(
                self.style.WARNING('No hay películas para procesar')
            )
            return
        
        success_count = 0
        error_count = 0
        
        for pelicula in peliculas:
            try:
                self.stdout.write(f"\n📽️ Procesando: {pelicula.titulo}")
                
                # Buscar trailer en YouTube
                trailers = youtube_service.search_movie_trailer(
                    pelicula.titulo, 
                    pelicula.ano_lanzamiento
                )
                
                if trailers:
                    # Tomar el primer resultado (más relevante)
                    best_trailer = trailers[0]
                    pelicula.trailer_youtube_id = best_trailer['youtube_id']
                    pelicula.save()
                    
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"   ✅ Trailer asignado: {best_trailer['title'][:50]}..."
                        )
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"   ❌ No se encontró trailer")
                    )
                
                # Pausa para no saturar la API
                time.sleep(0.5)
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"   🚫 Error: {str(e)}")
                )
        
        # Resumen final
        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Trailers asignados: {success_count}")
        )
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(f"❌ Errores: {error_count}")
            )
        self.stdout.write(
            self.style.SUCCESS(f"🎉 Proceso completado!")
        )