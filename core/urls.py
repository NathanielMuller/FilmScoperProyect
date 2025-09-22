from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('accion/', views.accion, name='accion'),
    path('comedia/', views.comedia, name='comedia'),
    path('documentales/', views.documentales, name='documentales'),
    path('romantica/', views.romantica, name='romantica'),
    path('terror/', views.terror, name='terror'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('pelicula/', views.pelicula, name='pelicula'),
]