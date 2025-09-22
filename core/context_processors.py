from .models import Categoria

def categorias_context(request):
    """Context processor que añade las categorías a todos los templates"""
    categorias = Categoria.objects.all().order_by('nombre')
    return {
        'categorias_nav': categorias
    }