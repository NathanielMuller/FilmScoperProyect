from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .forms import RegistroForm, LoginForm, ReseñaForm, PerfilForm
from .models import Pelicula, Categoria, Reseña, PerfilUsuario


def index(request):
    """Vista para la página principal"""
    return render(request, 'core/index.html')


def categoria(request, categoria_slug):
    """Vista dinámica para mostrar películas por categoría con paginación"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    peliculas_list = Pelicula.objects.filter(categorias=categoria, activa=True).order_by('-fecha_agregada')
    
    # Configurar paginación
    paginator = Paginator(peliculas_list, 12)  # 12 películas por página
    page = request.GET.get('page', 1)
    
    try:
        peliculas = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        peliculas = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página
        peliculas = paginator.page(paginator.num_pages)
    
    context = {
        'categoria': categoria,
        'peliculas': peliculas,
        'is_paginated': peliculas.has_other_pages(),
        'page_obj': peliculas,
    }
    
    return render(request, 'core/categoria.html', context)


# Mantener vistas específicas para compatibilidad con URLs existentes
def accion(request):
    """Vista para la categoría de acción - redirige a vista dinámica"""
    return categoria(request, 'accion')


def comedia(request):
    """Vista para la categoría de comedia - redirige a vista dinámica"""
    return categoria(request, 'comedia')


def documentales(request):
    """Vista para la categoría de documentales - redirige a vista dinámica"""
    return categoria(request, 'documentales')


def romantica(request):
    """Vista para la categoría de romance - redirige a vista dinámica"""
    return categoria(request, 'romantica')


def terror(request):
    """Vista para la categoría de terror - redirige a vista dinámica"""
    return categoria(request, 'terror')


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
            try:
                # Guardar el usuario
                user = form.save()
                
                # Obtener las credenciales para login automático
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                
                # Autenticar y loguear automáticamente
                authenticated_user = authenticate(request, username=username, password=raw_password)
                
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {authenticated_user.first_name}!')
                    return redirect('core:index')
                else:
                    # Si falla el login automático, mostrar mensaje de éxito pero pedir login manual
                    messages.success(request, 'Cuenta creada exitosamente. Por favor, inicia sesión con tus credenciales.')
                    return redirect('core:iniciar_sesion')
                    
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistroForm()
    
    return render(request, 'core/registro.html', {'form': form})


def recuperar_password(request):
    """Vista para recuperar contraseña"""
    # TODO: Implementar lógica de recuperación de contraseña
    return render(request, 'core/recuperar-password.html')


def pelicula(request):
    """Vista para detalle de película"""
    movie_slug = request.GET.get('movie')
    if not movie_slug:
        messages.error(request, 'No se especificó una película.')
        return redirect('core:index')
    
    try:
        pelicula = Pelicula.objects.get(slug=movie_slug, activa=True)
        
        # Obtener películas relacionadas de las mismas categorías
        categorias_pelicula = pelicula.categorias.all()
        peliculas_relacionadas = Pelicula.objects.filter(
            categorias__in=categorias_pelicula,
            activa=True
        ).exclude(id=pelicula.id).distinct()[:4]
        
        context = {
            'pelicula': pelicula,
            'peliculas_relacionadas': peliculas_relacionadas,
        }
        
        return render(request, 'core/pelicula.html', context)
        
    except Pelicula.DoesNotExist:
        messages.error(request, 'La película solicitada no existe.')
        return redirect('core:index')


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


@login_required
def mis_favoritos(request):
    """Vista para mostrar las películas favoritas del usuario"""
    try:
        perfil = request.user.perfil
        peliculas_favoritas = perfil.peliculas_favoritas.filter(activa=True).order_by('-fecha_agregada')
        
        # Configurar paginación
        paginator = Paginator(peliculas_favoritas, 12)  # 12 películas por página
        page = request.GET.get('page', 1)
        
        try:
            peliculas = paginator.page(page)
        except PageNotAnInteger:
            peliculas = paginator.page(1)
        except EmptyPage:
            peliculas = paginator.page(paginator.num_pages)
        
        context = {
            'titulo': 'Mis Favoritos',
            'descripcion': 'Películas que has marcado como favoritas',
            'peliculas': peliculas,
            'is_paginated': peliculas.has_other_pages(),
            'page_obj': peliculas,
            'tipo_lista': 'favoritos'
        }
        
        return render(request, 'core/lista_personal.html', context)
    
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de usuario.')
        return redirect('core:index')


@login_required
def ver_mas_tarde_lista(request):
    """Vista para mostrar las películas marcadas para ver más tarde"""
    try:
        perfil = request.user.perfil
        peliculas_ver_mas_tarde = perfil.ver_mas_tarde.filter(activa=True).order_by('-fecha_agregada')
        
        # Configurar paginación
        paginator = Paginator(peliculas_ver_mas_tarde, 12)  # 12 películas por página
        page = request.GET.get('page', 1)
        
        try:
            peliculas = paginator.page(page)
        except PageNotAnInteger:
            peliculas = paginator.page(1)
        except EmptyPage:
            peliculas = paginator.page(paginator.num_pages)
        
        context = {
            'titulo': 'Ver Más Tarde',
            'descripcion': 'Películas que has guardado para ver más tarde',
            'peliculas': peliculas,
            'is_paginated': peliculas.has_other_pages(),
            'page_obj': peliculas,
            'tipo_lista': 'ver_mas_tarde'
        }
        
        return render(request, 'core/lista_personal.html', context)
    
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de usuario.')
        return redirect('core:index')


@login_required
def toggle_favorito(request, pelicula_id):
    """Vista AJAX para agregar/quitar película de favoritos"""
    if request.method == 'POST':
        try:
            pelicula = get_object_or_404(Pelicula, id=pelicula_id)
            perfil = request.user.perfil
            
            if pelicula in perfil.peliculas_favoritas.all():
                # Quitar de favoritos
                perfil.peliculas_favoritas.remove(pelicula)
                es_favorito = False
                mensaje = f'"{pelicula.titulo}" eliminada de favoritos'
            else:
                # Agregar a favoritos
                perfil.peliculas_favoritas.add(pelicula)
                es_favorito = True
                mensaje = f'"{pelicula.titulo}" agregada a favoritos'
            
            return JsonResponse({
                'success': True,
                'es_favorito': es_favorito,
                'message': mensaje
            })
            
        except PerfilUsuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No se encontró tu perfil de usuario'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al procesar la solicitud'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def toggle_ver_mas_tarde_nuevo(request, pelicula_id):
    """Vista AJAX para agregar/quitar película de ver más tarde"""
    if request.method == 'POST':
        try:
            pelicula = get_object_or_404(Pelicula, id=pelicula_id)
            perfil = request.user.perfil
            
            if pelicula in perfil.ver_mas_tarde.all():
                # Quitar de ver más tarde
                perfil.ver_mas_tarde.remove(pelicula)
                en_lista = False
                mensaje = f'"{pelicula.titulo}" eliminada de "Ver más tarde"'
            else:
                # Agregar a ver más tarde
                perfil.ver_mas_tarde.add(pelicula)
                en_lista = True
                mensaje = f'"{pelicula.titulo}" agregada a "Ver más tarde"'
            
            return JsonResponse({
                'success': True,
                'en_lista': en_lista,
                'message': mensaje
            })
            
        except PerfilUsuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No se encontró tu perfil de usuario'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al procesar la solicitud'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
