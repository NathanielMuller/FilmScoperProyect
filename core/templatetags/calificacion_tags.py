from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def estrellas_visual(calificacion, max_estrellas=5):
    """
    Convierte una calificación numérica en estrellas visuales
    Uso: {{ pelicula.calificacion_promedio|estrellas_visual }}
    """
    try:
        calificacion = float(calificacion)
        estrellas_llenas = int(calificacion)
        media_estrella = (calificacion % 1) >= 0.5
        estrellas_vacias = max_estrellas - estrellas_llenas - (1 if media_estrella else 0)
        
        html = ""
        # Estrellas llenas
        for _ in range(estrellas_llenas):
            html += '<span class="text-warning">★</span>'
        
        # Media estrella
        if media_estrella:
            html += '<span class="text-warning">☆</span>'
        
        # Estrellas vacías
        for _ in range(estrellas_vacias):
            html += '<span class="text-muted">☆</span>'
        
        return mark_safe(html)
    except (ValueError, TypeError):
        return mark_safe('<span class="text-muted">☆☆☆☆☆</span>')

@register.filter
def estrellas_oficial_visual(calificacion_oficial):
    """
    Convierte calificación oficial (1-10) a estrellas visuales (1-5)
    """
    try:
        calificacion = float(calificacion_oficial)
        estrellas_equivalentes = (calificacion / 10) * 5
        return estrellas_visual(estrellas_equivalentes)
    except (ValueError, TypeError):
        return mark_safe('<span class="text-muted">☆☆☆☆☆</span>')

@register.simple_tag
def calificacion_badge(pelicula):
    """
    Genera un badge completo con ambas calificaciones
    """
    html = '<div class="calificacion-badges">'
    
    # Calificación oficial
    if pelicula.calificacion_oficial > 0:
        html += f'''
        <div class="badge-oficial mb-1">
            <span class="badge bg-warning text-dark me-1">
                🌟 {pelicula.calificacion_oficial:.1f}/10
            </span>
            <small class="text-muted">IMDb</small>
        </div>
        '''
    
    # Calificación FilmScoper
    if pelicula.calificacion_promedio > 0:
        html += f'''
        <div class="badge-filmscoper">
            <span class="badge bg-info text-white me-1">
                ⭐ {pelicula.calificacion_promedio:.1f}/5
            </span>
            <small class="text-muted">FilmScoper ({pelicula.total_calificaciones})</small>
        </div>
        '''
    else:
        html += '''
        <div class="badge-filmscoper">
            <span class="badge bg-secondary text-white me-1">
                ⭐ Sin calificar
            </span>
            <small class="text-muted">FilmScoper</small>
        </div>
        '''
    
    html += '</div>'
    return mark_safe(html)