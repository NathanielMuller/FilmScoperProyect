from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Categoria, Pelicula


class Command(BaseCommand):
    help = 'Poblar la base de datos con películas y categorías iniciales'

    def handle(self, *args, **options):
        # Crear categorías
        categorias_data = [
            {'nombre': 'Acción', 'slug': 'accion', 'descripcion': 'Películas llenas de aventura, persecuciones y espectáculo'},
            {'nombre': 'Comedia', 'slug': 'comedia', 'descripcion': 'Películas divertidas que te harán reír'},
            {'nombre': 'Documentales', 'slug': 'documentales', 'descripcion': 'Historias reales que te harán pensar'},
            {'nombre': 'Romance', 'slug': 'romantica', 'descripcion': 'Historias de amor que tocarán tu corazón'},
            {'nombre': 'Terror', 'slug': 'terror', 'descripcion': 'Películas que te mantendrán al borde del asiento'},
        ]

        categorias_creadas = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'nombre': cat_data['nombre'],
                    'descripcion': cat_data['descripcion']
                }
            )
            categorias_creadas[cat_data['slug']] = categoria
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Categoría creada: {categoria.nombre}')
                )

        # Datos de películas basados en el JavaScript
        peliculas_data = [
            # Acción
            {
                'titulo': '007: Skyfall',
                'slug': 'skyfall',
                'año': 2012,
                'duracion': 143,
                'director': 'Sam Mendes',
                'reparto': 'Daniel Craig, Javier Bardem, Naomie Harris, Judi Dench',
                'sinopsis': 'La lealtad de Bond hacia M se pone a prueba cuando su pasado regresa para atormentarla. Cuando MI6 es atacado, el Agente 007 debe localizar y destruir la amenaza, sin importar el costo personal que esto represente.',
                'poster': 'core/img/accion/007-skyfall.webp',
                'categorias': ['accion']
            },
            {
                'titulo': 'El Caballero Oscuro',
                'slug': 'el-caballero-oscuro',
                'año': 2008,
                'duracion': 152,
                'director': 'Christopher Nolan',
                'reparto': 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
                'sinopsis': 'Cuando la amenaza conocida como el Joker emerge de su misterioso pasado, causa estragos y caos en la gente de Gotham. Batman debe aceptar una de las pruebas psicológicas y físicas más grandes de su habilidad para luchar contra la injusticia.',
                'poster': 'core/img/accion/el-caballero-oscuro.webp',
                'categorias': ['accion']
            },
            {
                'titulo': 'Gladiador',
                'slug': 'gladiador',
                'año': 2000,
                'duracion': 155,
                'director': 'Ridley Scott',
                'reparto': 'Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed',
                'sinopsis': 'Un ex-general romano busca venganza contra el emperador corrupto que asesinó a su familia y lo envió a la esclavitud.',
                'poster': 'core/img/accion/gladiador.webp',
                'categorias': ['accion']
            },
            {
                'titulo': 'Mad Max: Fury Road',
                'slug': 'mad-max',
                'año': 2015,
                'duracion': 120,
                'director': 'George Miller',
                'reparto': 'Tom Hardy, Charlize Theron, Nicholas Hoult',
                'sinopsis': 'En un futuro apocalíptico, Max se alía con Furiosa para escapar de un tirano y su ejército en una guerra de carreteras de alta velocidad.',
                'poster': 'core/img/accion/mad-max.webp',
                'categorias': ['accion']
            },
            {
                'titulo': 'Vengadores: Endgame',
                'slug': 'vengadores-endgame',
                'año': 2019,
                'duracion': 181,
                'director': 'Anthony Russo, Joe Russo',
                'reparto': 'Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth',
                'sinopsis': 'Tras los devastadores eventos de Infinity War, los Vengadores supervivientes se unen una vez más para deshacer las acciones de Thanos.',
                'poster': 'core/img/accion/vengadores-endgame.webp',
                'categorias': ['accion']
            },

            # Comedia
            {
                'titulo': 'El Gran Hotel Budapest',
                'slug': 'gran-hotel-budapest',
                'año': 2014,
                'duracion': 99,
                'director': 'Wes Anderson',
                'reparto': 'Ralph Fiennes, F. Murray Abraham, Mathieu Amalric, Adrien Brody',
                'sinopsis': 'Las aventuras de Gustave H, un conserje legendario de un famoso hotel europeo, y Zero Moustafa, el botones que se convierte en su protegido más confiable.',
                'poster': 'core/img/comedia/gran-hotel-budapest.webp',
                'categorias': ['comedia']
            },
            {
                'titulo': 'Chicas Malas',
                'slug': 'chicas-malas',
                'año': 2004,
                'duracion': 97,
                'director': 'Mark Waters',
                'reparto': 'Lindsay Lohan, Rachel McAdams, Tina Fey, Amy Poehler',
                'sinopsis': 'Cady Heron es una adolescente que ha sido educada en casa en África por sus padres zoólogos. Cuando se muda a los suburbios de Illinois y comienza la escuela secundaria por primera vez, se encuentra navegando por las traicioneras aguas sociales de la vida adolescente.',
                'poster': 'core/img/comedia/chicas-malas.webp',
                'categorias': ['comedia']
            },
            {
                'titulo': '¿Dónde están las rubias?',
                'slug': 'donde-estan-las-rubias',
                'año': 2004,
                'duracion': 109,
                'director': 'Keenen Ivory Wayans',
                'reparto': 'Shawn Wayans, Marlon Wayans, Kerry Washington, John Heard',
                'sinopsis': 'Dos agentes del FBI se disfrazan como hermanas ricas y blancas para investigar una serie de secuestros.',
                'poster': 'core/img/comedia/donde-estan-las-rubias.webp',
                'categorias': ['comedia']
            },
            {
                'titulo': 'Superbad',
                'slug': 'supercool',
                'año': 2007,
                'duracion': 113,
                'director': 'Greg Mottola',
                'reparto': 'Jonah Hill, Michael Cera, Christopher Mintz-Plasse',
                'sinopsis': 'Dos amigos inseparables intentan conseguir alcohol para una fiesta antes de graduarse de la secundaria.',
                'poster': 'core/img/comedia/supercool.webp',
                'categorias': ['comedia']
            },
            {
                'titulo': 'Zoolander',
                'slug': 'zoolander',
                'año': 2001,
                'duracion': 90,
                'director': 'Ben Stiller',
                'reparto': 'Ben Stiller, Owen Wilson, Christine Taylor',
                'sinopsis': 'Un modelo masculino dimwit es lavado de cerebro para asesinar al primer ministro de Malasia.',
                'poster': 'core/img/comedia/zoolander.webp',
                'categorias': ['comedia']
            },

            # Documentales
            {
                'titulo': 'Free Solo',
                'slug': 'free-solo',
                'año': 2018,
                'duracion': 100,
                'director': 'Elizabeth Chai Vasarhelyi, Jimmy Chin',
                'reparto': 'Alex Honnold',
                'sinopsis': 'Sigue a Alex Honnold mientras se convierte en la primera persona en escalar El Capitán en el Parque Nacional Yosemite sin cuerdas ni equipo de seguridad, confiando únicamente en su habilidad física y fortaleza mental.',
                'poster': 'core/img/documentales/free-solo.webp',
                'categorias': ['documentales']
            },
            {
                'titulo': 'Mi Maestro el Pulpo',
                'slug': 'mi-maestro-pulpo',
                'año': 2020,
                'duracion': 85,
                'director': 'Pippa Ehrlich, James Reed',
                'reparto': 'Craig Foster',
                'sinopsis': 'Un cineasta desarrolla una relación extraordinaria con un pulpo que vive en un bosque de algas marinas en Sudáfrica.',
                'poster': 'core/img/documentales/mi-maestro-pulpo.webp',
                'categorias': ['documentales']
            },
            {
                'titulo': 'El Dilema Social',
                'slug': 'social-dilema',
                'año': 2020,
                'duracion': 94,
                'director': 'Jeff Orlowski',
                'reparto': 'Tristan Harris, Jeff Seibert, Bailey Richardson',
                'sinopsis': 'Explora el peligroso impacto humano de las redes sociales, con expertos en tecnología revelando cómo las plataformas manipulan a los usuarios.',
                'poster': 'core/img/documentales/social-dilema.webp',
                'categorias': ['documentales']
            },
            {
                'titulo': 'Fahrenheit 9/11',
                'slug': 'fahrenheit-911',
                'año': 2004,
                'duracion': 122,
                'director': 'Michael Moore',
                'reparto': 'Michael Moore, George W. Bush',
                'sinopsis': 'Michael Moore examina el ascenso al poder de George W. Bush y los eventos del 11 de septiembre.',
                'poster': 'core/img/documentales/fahrenheit-911.webp',
                'categorias': ['documentales']
            },
            {
                'titulo': 'El Viaje del Pingüino',
                'slug': 'el-viaje-del-pinguino',
                'año': 2005,
                'duracion': 80,
                'director': 'Luc Jacquet',
                'reparto': 'Morgan Freeman (narrador)',
                'sinopsis': 'Documenta el viaje anual de los pingüinos emperador en la Antártida.',
                'poster': 'core/img/documentales/el-viaje-del-pinguino.webp',
                'categorias': ['documentales']
            },

            # Romance
            {
                'titulo': 'Eterno Resplandor de una Mente sin Recuerdos',
                'slug': 'eterno-resplandor',
                'año': 2004,
                'duracion': 108,
                'director': 'Michel Gondry',
                'reparto': 'Jim Carrey, Kate Winslet, Kirsten Dunst, Mark Ruffalo',
                'sinopsis': 'Cuando su relación se vuelve agria, una pareja se somete a un procedimiento médico para eliminar de sus memorias todos los recuerdos el uno del otro.',
                'poster': 'core/img/romantica/eterno-resplandor.webp',
                'categorias': ['romantica']
            },
            {
                'titulo': 'Titanic',
                'slug': 'titanic',
                'año': 1997,
                'duracion': 194,
                'director': 'James Cameron',
                'reparto': 'Leonardo DiCaprio, Kate Winslet, Billy Zane, Gloria Stuart',
                'sinopsis': 'Una aristócrata de diecisiete años se enamora de un artista bondadoso pero pobre a bordo del lujoso y desafortunado R.M.S. Titanic.',
                'poster': 'core/img/romantica/titanic.webp',
                'categorias': ['romantica']
            },
            {
                'titulo': 'La La Land',
                'slug': 'lalaland',
                'año': 2016,
                'duracion': 128,
                'director': 'Damien Chazelle',
                'reparto': 'Ryan Gosling, Emma Stone, John Legend, Rosemarie DeWitt',
                'sinopsis': 'Una aspirante a actriz y un músico de jazz dedicado luchan por hacer realidad sus sueños en una ciudad conocida por destruir esperanzas y romper corazones.',
                'poster': 'core/img/romantica/lalaland.webp',
                'categorias': ['romantica']
            },
            {
                'titulo': 'Cuestión de Tiempo',
                'slug': 'cuestion-de-tiempo',
                'año': 2013,
                'duracion': 123,
                'director': 'Richard Curtis',
                'reparto': 'Domhnall Gleeson, Rachel McAdams, Bill Nighy',
                'sinopsis': 'Un joven descubre que puede viajar en el tiempo y lo usa para mejorar su vida amorosa.',
                'poster': 'core/img/romantica/cuestion-de-tiempo.webp',
                'categorias': ['romantica']
            },
            {
                'titulo': 'Vanilla Sky',
                'slug': 'vanilla-sky',
                'año': 2001,
                'duracion': 136,
                'director': 'Cameron Crowe',
                'reparto': 'Tom Cruise, Penélope Cruz, Cameron Diaz',
                'sinopsis': 'Un hombre adinerado lucha por separar la realidad de los sueños después de un accidente.',
                'poster': 'core/img/romantica/vanilla-sky.webp',
                'categorias': ['romantica']
            },

            # Terror
            {
                'titulo': 'The Babadook',
                'slug': 'babadook',
                'año': 2014,
                'duracion': 94,
                'director': 'Jennifer Kent',
                'reparto': 'Essie Davis, Noah Wiseman, Daniel Henshall',
                'sinopsis': 'Una madre viuda lucha con el comportamiento errático de su hijo de seis años. Pronto se dan cuenta de que algo siniestro los acecha.',
                'poster': 'core/img/terror/babadook.webp',
                'categorias': ['terror']
            },
            {
                'titulo': 'It Follows',
                'slug': 'it-follows',
                'año': 2014,
                'duracion': 100,
                'director': 'David Robert Mitchell',
                'reparto': 'Maika Monroe, Keir Gilchrist, Olivia Luccardi',
                'sinopsis': 'Una joven es perseguida por una presencia sobrenatural después de un encuentro sexual.',
                'poster': 'core/img/terror/it-follows.webp',
                'categorias': ['terror']
            },
            {
                'titulo': 'Hereditary',
                'slug': 'hereditary',
                'año': 2018,
                'duracion': 127,
                'director': 'Ari Aster',
                'reparto': 'Toni Collette, Milly Shapiro, Gabriel Byrne',
                'sinopsis': 'Una familia enfrenta secretos terribles después de la muerte de su matriarca.',
                'poster': 'core/img/terror/hereditary.webp',
                'categorias': ['terror']
            },
            {
                'titulo': 'El Exorcista',
                'slug': 'el-exorcista',
                'año': 1973,
                'duracion': 122,
                'director': 'William Friedkin',
                'reparto': 'Ellen Burstyn, Max von Sydow, Linda Blair',
                'sinopsis': 'Una niña de 12 años es poseída por una entidad demoníaca, y su madre busca ayuda de dos sacerdotes.',
                'poster': 'core/img/terror/el-exorcista-cover.webp',
                'categorias': ['terror']
            },
            {
                'titulo': 'El Conjuro',
                'slug': 'el-conjuro',
                'año': 2013,
                'duracion': 112,
                'director': 'James Wan',
                'reparto': 'Vera Farmiga, Patrick Wilson, Lili Taylor',
                'sinopsis': 'Los investigadores paranormales Ed y Lorraine Warren ayudan a una familia atormentada por una presencia oscura.',
                'poster': 'core/img/terror/el-conjuro.webp',
                'categorias': ['terror']
            },
            {
                'titulo': 'Pesadilla en Elm Street',
                'slug': 'pesadilla-elm-street',
                'año': 1984,
                'duracion': 91,
                'director': 'Wes Craven',
                'reparto': 'Heather Langenkamp, Johnny Depp, Robert Englund',
                'sinopsis': 'Un asesino quemado atormenta a los adolescentes de Springwood a través de sus sueños.',
                'poster': 'core/img/terror/pesadilla-en-elm-street.webp',
                'categorias': ['terror']
            },
        ]

        # Crear películas
        peliculas_creadas = 0
        for pelicula_data in peliculas_data:
            # Extraer categorías de la película
            categorias_nombres = pelicula_data.pop('categorias')
            
            # Crear o actualizar película
            pelicula, created = Pelicula.objects.get_or_create(
                slug=pelicula_data['slug'],
                defaults=pelicula_data
            )
            
            # Asignar categorías
            for cat_slug in categorias_nombres:
                if cat_slug in categorias_creadas:
                    pelicula.categorias.add(categorias_creadas[cat_slug])
            
            if created:
                peliculas_creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Película creada: {pelicula.titulo}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n¡Proceso completado!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Categorías: {len(categorias_creadas)}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Películas creadas: {peliculas_creadas}')
        )