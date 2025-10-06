from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .forms import RegistroForm, LoginForm, ReseñaForm, PerfilForm, ComentarioPeliculaForm
from .models import Pelicula, Categoria, Reseña, PerfilUsuario, ComentarioPelicula


def index(request):
    """Vista para la página principal con películas mejor rankeadas"""
    # Obtener las 12 películas mejor rankeadas según TMDB (calificacion_oficial)
    peliculas_top_ranked = Pelicula.objects.filter(
        activa=True,
        calificacion_oficial__gt=0  # Solo películas con calificación oficial
    ).order_by('-calificacion_oficial')[:12]
    
    context = {
        'peliculas_destacadas': peliculas_top_ranked,
    }
    
    return render(request, 'core/index.html', context)


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
        
        # Obtener reseñas de la película (sistema de rating)
        reseñas = Reseña.objects.filter(
            pelicula=pelicula, 
            activa=True
        ).select_related('usuario').order_by('-fecha_creacion')
        
        # Obtener reseña del usuario actual si está autenticado
        reseña_usuario = None
        formulario_reseña = None
        
        if request.user.is_authenticated:
            try:
                reseña_usuario = Reseña.objects.get(usuario=request.user, pelicula=pelicula)
                formulario_reseña = ReseñaForm(instance=reseña_usuario, user=request.user, pelicula=pelicula)
            except Reseña.DoesNotExist:
                formulario_reseña = ReseñaForm(user=request.user, pelicula=pelicula)
        
        # Obtener comentarios de la película (sistema de comentarios múltiples)
        comentarios = ComentarioPelicula.objects.filter(
            pelicula=pelicula, 
            respuesta_a=None
        ).select_related('usuario').prefetch_related('respuestas').order_by('-fecha_creacion')
        
        # Agregar rating de cada usuario a los comentarios
        for comentario in comentarios:
            try:
                resena_usuario = Reseña.objects.get(usuario=comentario.usuario, pelicula=pelicula)
                comentario.usuario_rating = resena_usuario.calificacion
            except Reseña.DoesNotExist:
                comentario.usuario_rating = None
        
        # Procesar formulario de comentarios
        formulario_comentario = None
        if request.user.is_authenticated:
            if request.method == 'POST' and 'contenido' in request.POST:
                # Verificar límites de comentarios
                comentarios_padre_usuario = ComentarioPelicula.objects.filter(
                    usuario=request.user,
                    pelicula=pelicula,
                    respuesta_a=None
                ).count()
                
                respuestas_usuario = ComentarioPelicula.objects.filter(
                    usuario=request.user,
                    pelicula=pelicula,
                    respuesta_a__isnull=False
                ).count()
                
                # Determinar si es respuesta o comentario padre
                respuesta_a_id = request.POST.get('respuesta_a')
                es_respuesta = respuesta_a_id is not None
                
                # Validar límites
                if es_respuesta and respuestas_usuario >= 10:
                    messages.error(request, 'Has alcanzado el límite de 10 respuestas por película.')
                    return redirect(request.path + f"?movie={movie_slug}")
                elif not es_respuesta and comentarios_padre_usuario >= 5:
                    messages.error(request, 'Has alcanzado el límite de 5 comentarios por película.')
                    return redirect(request.path + f"?movie={movie_slug}")
                
                formulario_comentario = ComentarioPeliculaForm(request.POST)
                if formulario_comentario.is_valid():
                    comentario = formulario_comentario.save(commit=False)
                    comentario.usuario = request.user
                    comentario.pelicula = pelicula
                    
                    # Si es respuesta, asignar el comentario padre
                    if es_respuesta:
                        try:
                            comentario_padre = ComentarioPelicula.objects.get(
                                id=respuesta_a_id,
                                pelicula=pelicula
                            )
                            comentario.respuesta_a = comentario_padre
                        except ComentarioPelicula.DoesNotExist:
                            messages.error(request, 'El comentario al que intentas responder no existe.')
                            return redirect(request.path + f"?movie={movie_slug}")
                    
                    comentario.save()
                    
                    mensaje_tipo = 'respuesta' if es_respuesta else 'comentario'
                    messages.success(request, f'¡{mensaje_tipo.capitalize()} agregado exitosamente!')
                    return redirect(request.path + f"?movie={movie_slug}")
            else:
                formulario_comentario = ComentarioPeliculaForm()
        
        # Obtener límites de comentarios para el usuario actual
        comentarios_limite_info = {}
        if request.user.is_authenticated:
            comentarios_padre_usuario = ComentarioPelicula.objects.filter(
                usuario=request.user,
                pelicula=pelicula,
                respuesta_a=None
            ).count()
            
            respuestas_usuario = ComentarioPelicula.objects.filter(
                usuario=request.user,
                pelicula=pelicula,
                respuesta_a__isnull=False
            ).count()
            
            comentarios_limite_info = {
                'comentarios_padre': comentarios_padre_usuario,
                'respuestas': respuestas_usuario,
                'limite_comentarios_padre': 5,
                'limite_respuestas': 10,
                'puede_comentar': comentarios_padre_usuario < 5,
                'puede_responder': respuestas_usuario < 10,
            }

        context = {
            'pelicula': pelicula,
            'peliculas_relacionadas': peliculas_relacionadas,
            'reseñas': reseñas,
            'reseña_usuario': reseña_usuario,
            'formulario_reseña': formulario_reseña,
            'comentarios': comentarios,
            'formulario_comentario': formulario_comentario,
            'comentarios_limite_info': comentarios_limite_info,
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
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Debes iniciar sesión para calificar'
            })
            
        pelicula = get_object_or_404(Pelicula, id=pelicula_id)
        
        try:
            # Obtener calificación desde JSON o POST data
            if request.content_type == 'application/json':
                import json
                data = json.loads(request.body)
                calificacion = int(data.get('calificacion', 0))
            else:
                calificacion = int(request.POST.get('calificacion', 0))
            
            # Validar calificación
            if calificacion < 1 or calificacion > 5:
                return JsonResponse({
                    'success': False,
                    'message': 'La calificación debe estar entre 1 y 5 estrellas'
                })
            
            # Crear o actualizar reseña del usuario (solo rating, sin comentario)
            reseña, created = Reseña.objects.get_or_create(
                usuario=request.user,
                pelicula=pelicula,
                defaults={'calificacion': calificacion, 'comentario': ''}
            )
            
            if not created:
                # Actualizar calificación existente
                reseña.calificacion = calificacion
                reseña.save()
                mensaje = f'Tu calificación ha sido actualizada a {calificacion}/5 estrellas'
            else:
                mensaje = f'Has calificado esta película con {calificacion}/5 estrellas'
            
            # Actualizar promedio de la película
            pelicula.actualizar_calificacion()
            
            return JsonResponse({
                'success': True,
                'message': mensaje,
                'calificacion_usuario': calificacion,
                'nueva_calificacion': pelicula.calificacion_promedio,
                'total_calificaciones': pelicula.total_calificaciones
            })
            
        except (ValueError, TypeError, json.JSONDecodeError):
            return JsonResponse({
                'success': False,
                'message': 'Calificación inválida'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al guardar la calificación'
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
