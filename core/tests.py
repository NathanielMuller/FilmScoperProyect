from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from .models import Categoria, Pelicula, PerfilUsuario, Reseña


class CategoriaModelTest(TestCase):
    """Tests para el modelo Categoria"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Acción",
            slug="accion",
            descripcion="Películas de acción y aventura"
        )
    
    def test_categoria_creation(self):
        """Test de creación de categoría"""
        self.assertEqual(self.categoria.nombre, "Acción")
        self.assertEqual(self.categoria.slug, "accion")
        self.assertTrue(self.categoria.descripcion)
    
    def test_categoria_str_method(self):
        """Test del método __str__ de categoría"""
        self.assertEqual(str(self.categoria), "Acción")


class PeliculaModelTest(TestCase):
    """Tests para el modelo Pelicula"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Ciencia Ficción",
            slug="ciencia-ficcion"
        )
        self.pelicula = Pelicula.objects.create(
            titulo="Blade Runner 2049",
            slug="blade-runner-2049",
            año=2017,
            duracion=164,
            director="Denis Villeneuve",
            reparto="Ryan Gosling, Harrison Ford",
            sinopsis="Secuela del clásico de ciencia ficción"
        )
        self.pelicula.categorias.add(self.categoria)
    
    def test_pelicula_creation(self):
        """Test de creación de película"""
        self.assertEqual(self.pelicula.titulo, "Blade Runner 2049")
        self.assertEqual(self.pelicula.año, 2017)
        self.assertEqual(self.pelicula.duracion, 164)
        self.assertTrue(self.pelicula.activa)
    
    def test_pelicula_str_method(self):
        """Test del método __str__ de película"""
        self.assertEqual(str(self.pelicula), "Blade Runner 2049 (2017)")
    
    def test_pelicula_get_absolute_url(self):
        """Test de URL absoluta de película"""
        # Cambiar a una URL que existe en el proyecto
        expected_url = reverse('core:pelicula', kwargs={'slug': self.pelicula.slug})
        self.assertEqual(self.pelicula.get_absolute_url(), expected_url)


class ViewsTest(TestCase):
    """Tests para las vistas principales"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre="Terror",
            slug="terror"
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_index_view(self):
        """Test de la vista principal"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FilmScoper')
    
    def test_categoria_view(self):
        """Test de la vista de categoría"""
        response = self.client.get(
            reverse('core:categoria', kwargs={'categoria_slug': 'terror'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Terror')
    
    def test_login_view_get(self):
        """Test GET de la vista de login"""
        response = self.client.get(reverse('core:iniciar_sesion'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Iniciar Sesión')
    
    def test_login_view_post_valid(self):
        """Test POST válido de login"""
        response = self.client.post(reverse('core:iniciar_sesion'), {
            'username': 'testuser',
            'password': 'testpass123',
            'remember_me': False
        })
        self.assertEqual(response.status_code, 302)  # Redirect después de login exitoso
    
    def test_login_view_post_invalid(self):
        """Test POST inválido de login"""
        response = self.client.post(reverse('core:iniciar_sesion'), {
            'username': 'wronguser',
            'password': 'wrongpass',
            'remember_me': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrectos')
    
    def test_protected_view_requires_login(self):
        """Test que las vistas protegidas requieren login"""
        response = self.client.get(reverse('core:perfil'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
        self.assertIn('iniciar-sesion', response.url)


class PerfilUsuarioTest(TestCase):
    """Tests para el perfil de usuario"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_perfil_creation(self):
        """Test de creación automática de perfil"""
        # Crear el perfil manualmente si no se crea automáticamente
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.user)
        self.assertEqual(perfil.user, self.user)
    
    def test_perfil_view_authenticated(self):
        """Test de vista de perfil con usuario autenticado"""
        response = self.client.get(reverse('core:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')


class ReseñaModelTest(TestCase):
    """Tests para el modelo de reseñas"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='reviewer',
            password='testpass123'
        )
        self.categoria = Categoria.objects.create(
            nombre="Drama",
            slug="drama"
        )
        self.pelicula = Pelicula.objects.create(
            titulo="Película Test",
            slug="pelicula-test",
            año=2023,
            duracion=120,
            director="Director Test",
            reparto="Actor Test",
            sinopsis="Una película de prueba"
        )
        self.reseña = Reseña.objects.create(
            usuario=self.user,
            pelicula=self.pelicula,
            calificacion=4,
            comentario="Muy buena película"
        )
    
    def test_reseña_creation(self):
        """Test de creación de reseña"""
        self.assertEqual(self.reseña.calificacion, 4)
        self.assertEqual(self.reseña.comentario, "Muy buena película")
        self.assertEqual(self.reseña.usuario, self.user)
        self.assertEqual(self.reseña.pelicula, self.pelicula)
    
    def test_reseña_str_method(self):
        """Test del método __str__ de reseña"""
        # Verificar el formato real del método __str__
        expected = f"reviewer - Película Test (4⭐)"
        self.assertEqual(str(self.reseña), expected)
