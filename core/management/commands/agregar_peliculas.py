from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Categoria, Pelicula


class Command(BaseCommand):
    help = 'Agregar nuevas películas a la base de datos'

    def handle(self, *args, **options):
        # Nuevas películas que quieres agregar
        nuevas_peliculas = [
            {
                'titulo': 'Dune',
                'slug': 'dune-2021',
                'año': 2021,
                'duracion': 155,
                'director': 'Denis Villeneuve',
                'reparto': 'Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Josh Brolin',
                'sinopsis': 'Paul Atreides, un joven brillante y talentoso nacido con un gran destino que está más allá de su comprensión, debe viajar al planeta más peligroso del universo para asegurar el futuro de su familia y su gente.',
                'poster': 'core/img/accion/dune.webp',  # Asegúrate de tener la imagen
                'categorias': ['accion']  # Puede ser múltiples categorías
            },
            {
                'titulo': 'Spider-Man: No Way Home',
                'slug': 'spiderman-no-way-home',
                'año': 2021,
                'duracion': 148,
                'director': 'Jon Watts',
                'reparto': 'Tom Holland, Zendaya, Benedict Cumberbatch, Willem Dafoe',
                'sinopsis': 'Peter Parker busca la ayuda del Doctor Strange para hacer que el mundo olvide que él es Spider-Man. Sin embargo, el hechizo no sale como esperaban.',
                'poster': 'core/img/accion/spiderman-no-way-home.webp',
                'categorias': ['accion']
            },
            {
                'titulo': 'Encanto',
                'slug': 'encanto',
                'año': 2021,
                'duracion': 102,
                'director': 'Jared Bush, Byron Howard',
                'reparto': 'Stephanie Beatriz, María Cecilia Botero, John Leguizamo',
                'sinopsis': 'Una niña extraordinaria de una familia mágica que vive en una casa mágica en las montañas de Colombia, en un lugar vibrante llamado Encanto.',
                'poster': 'core/img/comedia/encanto.webp',
                'categorias': ['comedia']  # También podría ser 'familiar' si creas esa categoría
            }
        ]

        # Obtener categorías existentes
        categorias_map = {cat.slug: cat for cat in Categoria.objects.all()}

        peliculas_agregadas = 0
        for pelicula_data in nuevas_peliculas:
            categorias_nombres = pelicula_data.pop('categorias')
            
            # Verificar si ya existe
            if Pelicula.objects.filter(slug=pelicula_data['slug']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Película ya existe: {pelicula_data["titulo"]}')
                )
                continue
            
            # Crear película
            pelicula = Pelicula.objects.create(**pelicula_data)
            
            # Asignar categorías
            for cat_slug in categorias_nombres:
                if cat_slug in categorias_map:
                    pelicula.categorias.add(categorias_map[cat_slug])
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Categoría no encontrada: {cat_slug}')
                    )
            
            peliculas_agregadas += 1
            self.stdout.write(
                self.style.SUCCESS(f'Película agregada: {pelicula.titulo}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n¡Agregadas {peliculas_agregadas} nuevas películas!')
        )