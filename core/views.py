from django.shortcuts import render


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
    """Vista para iniciar sesión"""
    return render(request, 'core/iniciar-sesion.html')


def registro(request):
    """Vista para registro de usuarios"""
    return render(request, 'core/registro.html')


def recuperar_password(request):
    """Vista para recuperar contraseña"""
    return render(request, 'core/recuperar-password.html')


def pelicula(request):
    """Vista para detalle de película"""
    return render(request, 'core/pelicula.html')
