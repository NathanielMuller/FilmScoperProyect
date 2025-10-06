from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Pelicula, Categoria
from .forms import PeliculaForm
from .services import tmdb_service
from datetime import datetime, date
from django.core.cache import cache


@staff_member_required
def buscar_portadas_admin(request):
    """
    Vista para buscar portadas en TMDB desde el panel de administración
    Solo accesible para staff
    """
    pelicula_id = request.GET.get('pelicula_id')
    pelicula = None
    
    if pelicula_id:
        try:
            pelicula = Pelicula.objects.get(id=pelicula_id)
        except Pelicula.DoesNotExist:
            messages.error(request, 'Película no encontrada')
            return redirect('admin:core_pelicula_changelist')
    
    context = {
        'pelicula': pelicula,
        'titulo': pelicula.titulo if pelicula else '',
        'año': pelicula.año if pelicula else '',
    }
    
    return render(request, 'admin/buscar_portadas_tmdb.html', context)


@staff_member_required
@csrf_exempt
def ajax_buscar_portadas(request):
    """
    Vista AJAX para buscar portadas en TMDB
    """
    if request.method == 'GET':
        titulo = request.GET.get('query', '').strip()  # Cambiado de 'titulo' a 'query'
        año = request.GET.get('año', '')
        
        if not titulo:
            return JsonResponse({
                'success': False,
                'message': 'El título es requerido'
            })
        
        try:
            print(f"DEBUG: Buscando película: '{titulo}', año: '{año}'")  # Debug
            
            # Incrementar contador de uso
            today = date.today().strftime('%Y-%m-%d')
            cache_key = f'tmdb_usage_{today}'
            current_usage = cache.get(cache_key, 0)
            cache.set(cache_key, current_usage + 1, 86400)  # 24 horas
            print(f"DEBUG: Contador incrementado a {current_usage + 1}")
            
            # Convertir año a entero si se proporciona
            year_int = None
            if año:
                try:
                    year_int = int(año)
                except ValueError:
                    pass
            
            # Buscar en TMDB
            print(f"DEBUG: Llamando a tmdb_service.search_movies('{titulo}', {year_int})")  # Debug
            resultados = tmdb_service.search_movies(titulo, year_int)
            print(f"DEBUG: Resultados obtenidos: {len(resultados) if resultados else 0}")  # Debug
            
            if resultados:
                return JsonResponse({
                    'success': True,
                    'resultados': resultados,
                    'total': len(resultados)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No se encontraron resultados en TMDB'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al consultar TMDB: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@staff_member_required
def ajax_asignar_portada(request):
    """
    Vista AJAX para asignar una portada de TMDB a una película
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pelicula_id = data.get('pelicula_id')
            poster_url = data.get('poster_url')
            tmdb_data = data.get('tmdb_data', {})
            
            if not pelicula_id or not poster_url:
                return JsonResponse({
                    'success': False,
                    'message': 'Datos incompletos'
                })
            
            # Obtener la película
            pelicula = Pelicula.objects.get(id=pelicula_id)
            
            # Por ahora, solo devolvemos la URL para copiar manualmente
            # En el futuro podrías implementar descarga automática
            
            return JsonResponse({
                'success': True,
                'message': 'Portada seleccionada exitosamente',
                'poster_url': poster_url,
                'tmdb_info': tmdb_data,
                'instrucciones': 'Copia la URL de la portada y pégala en el campo "Poster" del formulario de la película'
            })
            
        except Pelicula.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Película no encontrada'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@staff_member_required
@csrf_exempt
def ajax_obtener_detalles_completos(request):
    """
    Vista AJAX para obtener todos los detalles de una película de TMDB
    """
    if request.method == 'GET':
        tmdb_id = request.GET.get('tmdb_id')
        
        if not tmdb_id:
            return JsonResponse({
                'success': False,
                'message': 'ID de TMDB requerido'
            })
        
        try:
            print(f"DEBUG: Obteniendo detalles para TMDB ID: {tmdb_id}")  # Debug
            
            # Incrementar contador de uso
            today = date.today().strftime('%Y-%m-%d')
            cache_key = f'tmdb_usage_{today}'
            current_usage = cache.get(cache_key, 0)
            cache.set(cache_key, current_usage + 1, 86400)  # 24 horas
            print(f"DEBUG: Contador incrementado a {current_usage + 1}")
            
            # Obtener detalles completos de TMDB
            detalles = tmdb_service.get_movie_details(int(tmdb_id))
            print(f"DEBUG: Detalles obtenidos: {detalles is not None}")  # Debug
            
            if detalles:
                return JsonResponse({
                    'success': True,
                    'detalles': detalles,
                    'message': 'Detalles obtenidos exitosamente'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No se pudieron obtener los detalles de TMDB'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al obtener detalles: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@staff_member_required
def agregar_pelicula_con_tmdb(request):
    """
    Vista para agregar película con autocompletado de TMDB
    """
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            pelicula = form.save()
            messages.success(request, f'Película "{pelicula.titulo}" creada exitosamente.')
            return redirect('tmdb_agregar_pelicula')  # Redirigir a la misma página para añadir otra
        else:
            messages.error(request, 'Hay errores en el formulario. Revisa los datos.')
    else:
        form = PeliculaForm()
    
    # Obtener categorías para el selector
    categorias = Categoria.objects.all()
    
    context = {
        'form': form,
        'categorias': categorias,
        'title': 'Agregar Película con TMDB'
    }
    
    return render(request, 'core/admin/agregar_pelicula_tmdb.html', context)


@staff_member_required
def ajax_tmdb_usage_counter(request):
    """
    Vista AJAX para obtener el contador de uso diario de TMDB
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    today = date.today().strftime('%Y-%m-%d')
    cache_key = f'tmdb_usage_{today}'
    
    # Obtener el contador del día desde cache (simula el tracking real)
    daily_usage = cache.get(cache_key, 0)
    
    # Límites de TMDB API gratuita
    DAILY_LIMIT = 1000  # requests por día
    REQUESTS_PER_MOVIE = 2  # búsqueda + detalles
    
    # Calcular películas disponibles
    movies_available_daily = (DAILY_LIMIT - daily_usage) // REQUESTS_PER_MOVIE
    movies_available_session = 20  # 40 requests / 2 = 20 películas por sesión de 10s
    
    # Determinar estado del contador
    usage_percentage = (daily_usage / DAILY_LIMIT) * 100
    
    if usage_percentage >= 90:
        status = 'danger'
    elif usage_percentage >= 70:
        status = 'warning'
    else:
        status = 'success'
    
    return JsonResponse({
        'success': True,
        'daily': {
            'used': daily_usage,
            'limit': DAILY_LIMIT,
            'remaining': DAILY_LIMIT - daily_usage,
            'movies_available': max(0, movies_available_daily)
        },
        'session': {
            'movies_available': movies_available_session
        },
        'status': status,
        'percentage': round(usage_percentage, 1)
    })
    
    return render(request, 'core/admin/agregar_pelicula_tmdb.html', context)