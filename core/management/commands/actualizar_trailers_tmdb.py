from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Pelicula
from core.services import tmdb_service
import time


class Command(BaseCommand):
    help = 'Actualizar trailers y posters de películas usando TMDB API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--todas',
            action='store_true',
            help='Actualizar todas las películas, incluso las que ya tienen datos'
        )
        parser.add_argument(
            '--limite',
            type=int,
            default=None,
            help='Número máximo de películas a procesar'
        )
        parser.add_argument(
            '--solo-trailers',
            action='store_true',
            help='Solo actualizar trailers, no posters'
        )
        parser.add_argument(
            '--solo-posters',
            action='store_true',
            help='Solo actualizar posters, no trailers'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando actualización de trailers desde TMDB...\n')
        )

        # Determinar qué películas procesar
        if options['todas']:
            peliculas = Pelicula.objects.filter(activa=True)
            self.stdout.write("Procesando TODAS las películas activas...")
        else:
            # Por defecto, solo películas sin trailer
            peliculas = Pelicula.objects.filter(
                activa=True, 
                trailer_youtube_id__in=['', None]
            )
            self.stdout.write("Procesando solo películas SIN trailer...")

        # Aplicar límite si se especifica
        if options['limite']:
            peliculas = peliculas[:options['limite']]
            self.stdout.write(f"Limitando a {options['limite']} películas")

        total_peliculas = peliculas.count()
        self.stdout.write(f"Total de películas a procesar: {total_peliculas}\n")

        if total_peliculas == 0:
            self.stdout.write(
                self.style.WARNING('No hay películas para procesar.')
            )
            return

        # Contadores
        actualizadas = 0
        errores = 0
        sin_trailer = 0

        for i, pelicula in enumerate(peliculas, 1):
            self.stdout.write(
                f"[{i}/{total_peliculas}] Procesando: {pelicula.titulo} ({pelicula.año})"
            )

            try:
                # Buscar la película en TMDB primero
                resultados_busqueda = tmdb_service.search_movies(
                    pelicula.titulo, 
                    pelicula.año, 
                    limit=1
                )

                if not resultados_busqueda:
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ No encontrada en TMDB: {pelicula.titulo}")
                    )
                    errores += 1
                    continue

                tmdb_id = resultados_busqueda[0].get('tmdb_id')
                if not tmdb_id:
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Sin ID de TMDB: {pelicula.titulo}")
                    )
                    errores += 1
                    continue

                # Obtener videos de TMDB
                videos_data = tmdb_service.get_movie_videos(tmdb_id)

                if not videos_data or not videos_data.get('trailer_youtube_id'):
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  Sin trailer en TMDB: {pelicula.titulo}")
                    )
                    sin_trailer += 1
                    continue

                trailer_id = videos_data['trailer_youtube_id']
                trailer_name = videos_data.get('trailer_name', 'Trailer')

                # Actualizar la película
                with transaction.atomic():
                    pelicula.trailer_youtube_id = trailer_id
                    pelicula.save(update_fields=['trailer_youtube_id'])

                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Actualizada: {trailer_name} ({trailer_id})")
                )
                actualizadas += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  ❌ Error: {pelicula.titulo} - {str(e)}")
                )
                errores += 1

            # Pausa para no sobrecargar la API
            if i % 10 == 0:
                self.stdout.write("  ⏸️  Pausa de 2 segundos...")
                time.sleep(2)

        # Resumen final
        self.stdout.write(f"\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"RESUMEN DE ACTUALIZACIÓN:"))
        self.stdout.write(f"Total procesadas: {total_peliculas}")
        self.stdout.write(self.style.SUCCESS(f"✅ Actualizadas exitosamente: {actualizadas}"))
        self.stdout.write(self.style.WARNING(f"⚠️  Sin trailer disponible: {sin_trailer}"))
        self.stdout.write(self.style.ERROR(f"❌ Errores: {errores}"))
        
        if actualizadas > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n¡{actualizadas} películas ahora tienen trailers de TMDB!")
            )