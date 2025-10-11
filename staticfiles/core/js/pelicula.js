// Base de datos de películas
const moviesDatabase = {
    'skyfall': {
        title: '007: Skyfall',
        year: '2012',
        duration: '143 min',
        genre: 'Acción, Thriller',
        rating: '⭐ 7.8/10',
        director: 'Sam Mendes',
        cast: 'Daniel Craig, Javier Bardem, Naomie Harris, Judi Dench',
        synopsis: 'La lealtad de Bond hacia M se pone a prueba cuando su pasado regresa para atormentarla. Cuando MI6 es atacado, el Agente 007 debe localizar y destruir la amenaza, sin importar el costo personal que esto represente.',
        poster: '/static/core/img/accion/007-skyfall.webp',
        category: 'accion'
    },
    'chicas-malas': {
        title: 'Chicas Malas',
        year: '2004',
        duration: '97 min',
        genre: 'Comedia, Drama',
        rating: '⭐ 7.0/10',
        director: 'Mark Waters',
        cast: 'Lindsay Lohan, Rachel McAdams, Tina Fey, Amy Poehler',
        synopsis: 'Cady Heron es una adolescente que ha sido educada en casa en África por sus padres zoólogos. Cuando se muda a los suburbios de Illinois y comienza la escuela secundaria por primera vez, se encuentra navegando por las traicioneras aguas sociales de la vida adolescente.',
        poster: '/static/core/img/comedia/chicas-malas.webp',
        category: 'comedia'
    },
    'free-solo': {
        title: 'Free Solo',
        year: '2018',
        duration: '100 min',
        genre: 'Documental, Deportes',
        rating: '⭐ 8.1/10',
        director: 'Elizabeth Chai Vasarhelyi, Jimmy Chin',
        cast: 'Alex Honnold',
        synopsis: 'Sigue a Alex Honnold mientras se convierte en la primera persona en escalar El Capitán en el Parque Nacional Yosemite sin cuerdas ni equipo de seguridad, confiando únicamente en su habilidad física y fortaleza mental.',
        poster: '/static/core/img/documentales/free-solo.webp',
        category: 'documentales'
    },
    'eterno-resplandor': {
        title: 'Eterno Resplandor de una Mente sin Recuerdos',
        year: '2004',
        duration: '108 min',
        genre: 'Romance, Drama, Sci-Fi',
        rating: '⭐ 8.3/10',
        director: 'Michel Gondry',
        cast: 'Jim Carrey, Kate Winslet, Kirsten Dunst, Mark Ruffalo',
        synopsis: 'Cuando su relación se vuelve agria, una pareja se somete a un procedimiento médico para eliminar de sus memorias todos los recuerdos el uno del otro.',
        poster: '/static/core/img/romantica/eterno-resplandor.webp',
        category: 'romance'
    },
    'babadook': {
        title: 'The Babadook',
        year: '2014',
        duration: '94 min',
        genre: 'Terror, Drama',
        rating: '⭐ 6.8/10',
        director: 'Jennifer Kent',
        cast: 'Essie Davis, Noah Wiseman, Daniel Henshall',
        synopsis: 'Una madre viuda lucha con el comportamiento errático de su hijo de seis años. Pronto se dan cuenta de que algo siniestro los acecha.',
        poster: '/static/core/img/terror/babadook.webp',
        category: 'terror'
    },
    'gladiador': {
        title: 'Gladiador',
        year: '2000',
        duration: '155 min',
        genre: 'Acción, Drama, Historia',
        rating: '⭐ 8.5/10',
        director: 'Ridley Scott',
        cast: 'Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed',
        synopsis: 'Un ex-general romano busca venganza contra el emperador corrupto que asesinó a su familia y lo envió a la esclavitud.',
        poster: '/static/core/img/accion/gladiador.webp',
        category: 'accion'
    },
    'titanic': {
        title: 'Titanic',
        year: '1997',
        duration: '194 min',
        genre: 'Romance, Drama',
        rating: '⭐ 7.9/10',
        director: 'James Cameron',
        cast: 'Leonardo DiCaprio, Kate Winslet, Billy Zane, Gloria Stuart',
        synopsis: 'Una aristócrata de diecisiete años se enamora de un artista bondadoso pero pobre a bordo del lujoso y desafortunado R.M.S. Titanic.',
        poster: '/static/core/img/romantica/titanic.webp',
        category: 'romance'
    },
    'gran-hotel-budapest': {
        title: 'El Gran Hotel Budapest',
        year: '2014',
        duration: '99 min',
        genre: 'Comedia, Drama',
        rating: '⭐ 8.1/10',
        director: 'Wes Anderson',
        cast: 'Ralph Fiennes, F. Murray Abraham, Mathieu Amalric, Adrien Brody',
        synopsis: 'Las aventuras de Gustave H, un conserje legendario de un famoso hotel europeo, y Zero Moustafa, el botones que se convierte en su protegido más confiable.',
        poster: '/static/core/img/comedia/gran-hotel-budapest.webp',
        category: 'comedia'
    },
    'el-caballero-oscuro': {
        title: 'El Caballero Oscuro',
        year: '2008',
        duration: '152 min',
        genre: 'Acción, Crime, Drama',
        rating: '⭐ 9.0/10',
        director: 'Christopher Nolan',
        cast: 'Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine',
        synopsis: 'Cuando la amenaza conocida como el Joker emerge de su misterioso pasado, causa estragos y caos en la gente de Gotham. Batman debe aceptar una de las pruebas psicológicas y físicas más grandes de su habilidad para luchar contra la injusticia.',
        poster: '/static/core/img/accion/el-caballero-oscuro.webp',
        category: 'accion'
    },
    'donde-estan-las-rubias': {
        title: '¿Dónde están las rubias?',
        year: '2004',
        duration: '109 min',
        genre: 'Comedia',
        rating: '⭐ 5.8/10',
        director: 'Keenen Ivory Wayans',
        cast: 'Shawn Wayans, Marlon Wayans, Kerry Washington, John Heard',
        synopsis: 'Dos agentes del FBI se disfrazan como hermanas ricas y blancas para investigar una serie de secuestros.',
        poster: '/static/core/img/comedia/donde-estan-las-rubias.webp',
        category: 'comedia'
    },
    'social-dilema': {
        title: 'El Dilema Social',
        year: '2020',
        duration: '94 min',
        genre: 'Documental',
        rating: '⭐ 7.6/10',
        director: 'Jeff Orlowski',
        cast: 'Tristan Harris, Jeff Seibert, Bailey Richardson',
        synopsis: 'Explora el peligroso impacto humano de las redes sociales, con expertos en tecnología revelando cómo las plataformas manipulan a los usuarios.',
        poster: '/static/core/img/documentales/social-dilema.webp',
        category: 'documentales'
    },
    'lalaland': {
        title: 'La La Land',
        year: '2016',
        duration: '128 min',
        genre: 'Romance, Musical, Drama',
        rating: '⭐ 8.0/10',
        director: 'Damien Chazelle',
        cast: 'Ryan Gosling, Emma Stone, John Legend, Rosemarie DeWitt',
        synopsis: 'Una aspirante a actriz y un músico de jazz dedicado luchan por hacer realidad sus sueños en una ciudad conocida por destruir esperanzas y romper corazones.',
        poster: '/static/core/img/romantica/lalaland.webp',
        category: 'romance'
    },
    // Películas adicionales de Acción
    'mad-max': {
        title: 'Mad Max: Fury Road',
        year: '2015',
        duration: '120 min',
        genre: 'Acción, Aventura',
        rating: '⭐ 8.1/10',
        director: 'George Miller',
        cast: 'Tom Hardy, Charlize Theron, Nicholas Hoult',
        synopsis: 'En un futuro apocalíptico, Max se alía con Furiosa para escapar de un tirano y su ejército en una guerra de carreteras de alta velocidad.',
        poster: '/static/core/img/accion/mad-max.webp',
        category: 'accion'
    },
    'vengadores-endgame': {
        title: 'Vengadores: Endgame',
        year: '2019',
        duration: '181 min',
        genre: 'Acción, Aventura, Sci-Fi',
        rating: '⭐ 8.4/10',
        director: 'Anthony Russo, Joe Russo',
        cast: 'Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth',
        synopsis: 'Tras los devastadores eventos de Infinity War, los Vengadores supervivientes se unen una vez más para deshacer las acciones de Thanos.',
        poster: '/static/core/img/accion/vengadores-endgame.webp',
        category: 'accion'
    },
    // Películas adicionales de Comedia
    'supercool': {
        title: 'Superbad',
        year: '2007',
        duration: '113 min',
        genre: 'Comedia',
        rating: '⭐ 7.6/10',
        director: 'Greg Mottola',
        cast: 'Jonah Hill, Michael Cera, Christopher Mintz-Plasse',
        synopsis: 'Dos amigos inseparables intentan conseguir alcohol para una fiesta antes de graduarse de la secundaria.',
        poster: '/static/core/img/comedia/supercool.webp',
        category: 'comedia'
    },
    'zoolander': {
        title: 'Zoolander',
        year: '2001',
        duration: '90 min',
        genre: 'Comedia',
        rating: '⭐ 6.5/10',
        director: 'Ben Stiller',
        cast: 'Ben Stiller, Owen Wilson, Christine Taylor',
        synopsis: 'Un modelo masculino dimwit es lavado de cerebro para asesinar al primer ministro de Malasia.',
        poster: '/static/core/img/comedia/zoolander.webp',
        category: 'comedia'
    },
    // Películas adicionales de Documentales
    'mi-maestro-pulpo': {
        title: 'Mi Maestro el Pulpo',
        year: '2020',
        duration: '85 min',
        genre: 'Documental, Naturaleza',
        rating: '⭐ 8.1/10',
        director: 'Pippa Ehrlich, James Reed',
        cast: 'Craig Foster',
        synopsis: 'Un cineasta desarrolla una relación extraordinaria con un pulpo que vive en un bosque de algas marinas en Sudáfrica.',
        poster: '/static/core/img/documentales/mi-maestro-pulpo.webp',
        category: 'documentales'
    },
    'fahrenheit-911': {
        title: 'Fahrenheit 9/11',
        year: '2004',
        duration: '122 min',
        genre: 'Documental, Político',
        rating: '⭐ 7.5/10',
        director: 'Michael Moore',
        cast: 'Michael Moore, George W. Bush',
        synopsis: 'Michael Moore examina el ascenso al poder de George W. Bush y los eventos del 11 de septiembre.',
        poster: '/static/core/img/documentales/fahrenheit-911.webp',
        category: 'documentales'
    },
    'el-viaje-del-pinguino': {
        title: 'El Viaje del Pingüino',
        year: '2005',
        duration: '80 min',
        genre: 'Documental, Naturaleza',
        rating: '⭐ 7.5/10',
        director: 'Luc Jacquet',
        cast: 'Morgan Freeman (narrador)',
        synopsis: 'Documenta el viaje anual de los pingüinos emperador en la Antártida.',
        poster: '/static/core/img/documentales/el-viaje-del-pinguino.webp',
        category: 'documentales'
    },
    // Películas adicionales de Romance
    'cuestion-de-tiempo': {
        title: 'Cuestión de Tiempo',
        year: '2013',
        duration: '123 min',
        genre: 'Romance, Drama, Comedia',
        rating: '⭐ 7.8/10',
        director: 'Richard Curtis',
        cast: 'Domhnall Gleeson, Rachel McAdams, Bill Nighy',
        synopsis: 'Un joven descubre que puede viajar en el tiempo y lo usa para mejorar su vida amorosa.',
        poster: '/static/core/img/romantica/cuestion-de-tiempo.webp',
        category: 'romance'
    },
    'vanilla-sky': {
        title: 'Vanilla Sky',
        year: '2001',
        duration: '136 min',
        genre: 'Romance, Thriller, Sci-Fi',
        rating: '⭐ 6.9/10',
        director: 'Cameron Crowe',
        cast: 'Tom Cruise, Penélope Cruz, Cameron Diaz',
        synopsis: 'Un hombre adinerado lucha por separar la realidad de los sueños después de un accidente.',
        poster: '/static/core/img/romantica/vanilla-sky.webp',
        category: 'romance'
    },
    // Películas adicionales de Terror
    'it-follows': {
        title: 'It Follows',
        year: '2014',
        duration: '100 min',
        genre: 'Terror, Thriller',
        rating: '⭐ 6.8/10',
        director: 'David Robert Mitchell',
        cast: 'Maika Monroe, Keir Gilchrist, Olivia Luccardi',
        synopsis: 'Una joven es perseguida por una presencia sobrenatural después de un encuentro sexual.',
        poster: '/static/core/img/terror/it-follows.webp',
        category: 'terror'
    },
    'hereditary': {
        title: 'Hereditary',
        year: '2018',
        duration: '127 min',
        genre: 'Terror, Drama, Thriller',
        rating: '⭐ 7.3/10',
        director: 'Ari Aster',
        cast: 'Toni Collette, Milly Shapiro, Gabriel Byrne',
        synopsis: 'Una familia enfrenta secretos terribles después de la muerte de su matriarca.',
        poster: '/static/core/img/terror/hereditary.webp',
        category: 'terror'
    },
    'el-exorcista': {
        title: 'El Exorcista',
        year: '1973',
        duration: '122 min',
        genre: 'Terror, Drama',
        rating: '⭐ 8.1/10',
        director: 'William Friedkin',
        cast: 'Ellen Burstyn, Max von Sydow, Linda Blair',
        synopsis: 'Una niña de 12 años es poseída por una entidad demoníaca, y su madre busca ayuda de dos sacerdotes.',
        poster: '/static/core/img/terror/el-exorcista-cover.webp',
        category: 'terror'
    },
    'el-conjuro': {
        title: 'El Conjuro',
        year: '2013',
        duration: '112 min',
        genre: 'Terror, Thriller',
        rating: '⭐ 7.5/10',
        director: 'James Wan',
        cast: 'Vera Farmiga, Patrick Wilson, Lili Taylor',
        synopsis: 'Los investigadores paranormales Ed y Lorraine Warren ayudan a una familia atormentada por una presencia oscura.',
        poster: '/static/core/img/terror/el-conjuro.webp',
        category: 'terror'
    },
    'pesadilla-elm-street': {
        title: 'Pesadilla en Elm Street',
        year: '1984',
        duration: '91 min',
        genre: 'Terror, Thriller',
        rating: '⭐ 7.4/10',
        director: 'Wes Craven',
        cast: 'Heather Langenkamp, Johnny Depp, Robert Englund',
        synopsis: 'Un asesino quemado atormenta a los adolescentes de Springwood a través de sus sueños.',
        poster: '/static/core/img/terror/pesadilla-en-elm-street.webp',
        category: 'terror'
    }
};

// Función para obtener parámetros de la URL
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Función para cargar la información de la película
function loadMovieInfo() {
    const movieId = getUrlParameter('movie');
    const movie = moviesDatabase[movieId];
    
    if (movie) {
        document.getElementById('movieTitle').textContent = movie.title;
        document.getElementById('movieYear').textContent = movie.year;
        document.getElementById('movieDuration').textContent = movie.duration;
        document.getElementById('movieGenre').textContent = movie.genre;
        document.getElementById('movieRating').textContent = movie.rating;
        document.getElementById('movieDirector').textContent = movie.director;
        document.getElementById('movieCast').textContent = movie.cast;
        document.getElementById('movieSynopsis').textContent = movie.synopsis;
        document.getElementById('moviePoster').src = movie.poster;
        document.getElementById('moviePoster').alt = movie.title;
        
        // Actualizar el título de la página
        document.title = `FilmScoper - ${movie.title}`;
        
        // Cargar películas relacionadas
        loadRelatedMovies(movie.category, movieId);
    } else {
        // Si no se encuentra la película, mostrar mensaje de error
        document.getElementById('movieTitle').textContent = 'Película no encontrada';
        document.getElementById('movieSynopsis').textContent = 'La película solicitada no existe en nuestra base de datos.';
    }
}

// Función para cargar películas relacionadas
function loadRelatedMovies(category, currentMovieId) {
    const relatedContainer = document.getElementById('relatedMovies');
    const relatedMovies = Object.entries(moviesDatabase)
        .filter(([id, movie]) => movie.category === category && id !== currentMovieId)
        .slice(0, 4); // Mostrar máximo 4 películas relacionadas
    
    relatedContainer.innerHTML = '';
    
    relatedMovies.forEach(([id, movie]) => {
        const movieCard = `
            <div class="col-6 col-md-3 mb-3">
                <a href="/pelicula/?movie=${id}" class="text-decoration-none">
                    <div class="card shadow-sm h-100">
                        <img src="${movie.poster}" class="card-img-top" alt="${movie.title}" style="height: 300px; object-fit: cover;">
                        <div class="card-body p-2">
                            <h6 class="card-title text-dark mb-1" style="font-size: 0.9rem;">${movie.title}</h6>
                            <p class="card-text text-muted mb-1" style="font-size: 0.8rem;">${movie.year}</p>
                            <p class="card-text text-warning" style="font-size: 0.8rem;">${movie.rating}</p>
                        </div>
                    </div>
                </a>
            </div>
        `;
        relatedContainer.innerHTML += movieCard;
    });
}

// Cargar la información cuando se carga la página
window.addEventListener('DOMContentLoaded', loadMovieInfo);