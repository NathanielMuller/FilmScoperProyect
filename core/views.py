from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from .forms import RegistroForm, LoginForm, ReseñaForm, PerfilForm
from .models import Pelicula, Categoria, Reseña, PerfilUsuario


def index(request):
    """Vista para la página principal"""
    return render(request, 'core/index.html')


def accion(request):
    """Vista para la categoría de acción"""
    return render(request, 'core/accion.html')


def comedia(request):
    """Vista para la categoría de comedia"""
    return render(request, 'core/comedia.html')


def documentales(request):
    """Vista para la categoría de documentales"""
    return render(request, 'core/documentales.html')


def romantica(request):
    """Vista para la categoría de romance"""
    return render(request, 'core/romantica.html')


def terror(request):
    """Vista para la categoría de terror"""
    return render(request, 'core/terror.html')


def iniciar_sesion(request):
    """Vista para iniciar sesión con validación híbrida"""
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            # Intentar autenticar por username
            user = authenticate(request, username=username_or_email, password=password)
            
            # Si no funciona, intentar por email
            if user is None:
                try:
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                
                # Configurar duración de sesión
                if not remember_me:
                    request.session.set_expiry(0)  # Expira al cerrar navegador
                
                messages.success(request, f'¡Bienvenido de vuelta, {user.first_name or user.username}!')
                
                # Redirigir a la página solicitada o al inicio
                next_url = request.GET.get('next', 'core:index')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'core/iniciar-sesion.html', {'form': form})


def registro(request):
    """Vista para registro de usuarios con validación híbrida"""
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Autenticar automáticamente después del registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {user.first_name}!')
                return redirect('core:index')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()
    
    return render(request, 'core/registro.html', {'form': form})


def recuperar_password(request):
    """Vista para recuperar contraseña"""
    # TODO: Implementar lógica de recuperación de contraseña
    return render(request, 'core/recuperar-password.html')


def pelicula(request):
    """Vista para detalle de película"""
    return render(request, 'core/pelicula.html')


def cerrar_sesion(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('core:index')


@login_required
def perfil(request):
    """Vista para ver/editar perfil de usuario"""
    try:
        perfil_usuario = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        # Crear perfil si no existe
        perfil_usuario = PerfilUsuario.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado exitosamente!')
            return redirect('core:perfil')
    else:
        form = PerfilForm(instance=perfil_usuario, user=request.user)
    
    return render(request, 'core/perfil.html', {'form': form, 'perfil': perfil_usuario})


@login_required
def calificar_pelicula(request, pelicula_id):
    """Vista para calificar una película (AJAX)"""
    if request.method == 'POST':
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        
        # Verificar si ya existe una reseña del usuario
        reseña, created = Reseña.objects.get_or_create(
            usuario=request.user,
            pelicula=pelicula,
            defaults={'calificacion': 1, 'comentario': ''}
        )
        
        form = ReseñaForm(request.POST, instance=reseña, user=request.user, pelicula=pelicula)
        if form.is_valid():
            form.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Calificación guardada exitosamente',
                'nueva_calificacion': pelicula.calificacion_promedio,
                'total_calificaciones': pelicula.total_calificaciones
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def toggle_favorito(request, pelicula_id):
    """Vista para agregar/quitar de favoritos (AJAX)"""
    if request.method == 'POST':
        from .models import ListaFavoritos
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        
        favorito, created = ListaFavoritos.objects.get_or_create(
            usuario=request.user,
            pelicula=pelicula
        )
        
        if not created:
            favorito.delete()
            es_favorito = False
            mensaje = 'Película eliminada de favoritos'
        else:
            es_favorito = True
            mensaje = 'Película agregada a favoritos'
        
        return JsonResponse({
            'success': True,
            'es_favorito': es_favorito,
            'message': mensaje
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def toggle_ver_mas_tarde(request, pelicula_id):
    """Vista para agregar/quitar de ver más tarde (AJAX)"""
    if request.method == 'POST':
        from .models import ListaVerMasTarde
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        
        item, created = ListaVerMasTarde.objects.get_or_create(
            usuario=request.user,
            pelicula=pelicula
        )
        
        if not created:
            item.delete()
            en_lista = False
            mensaje = 'Película eliminada de "Ver más tarde"'
        else:
            en_lista = True
            mensaje = 'Película agregada a "Ver más tarde"'
        
        return JsonResponse({
            'success': True,
            'en_lista': en_lista,
            'message': mensaje
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
