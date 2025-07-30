from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_view, name='menu'),
    path('seleccionar-nivel/', views.seleccionar_nivel_view, name='seleccionar_nivel'),
    path('tablero/<int:juego_id>/', views.tablero_view, name='tablero'),
]
