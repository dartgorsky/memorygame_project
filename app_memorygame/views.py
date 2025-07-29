# app_memorygame/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .logica import iniciar_partida
from .models import Game
from django.utils.timezone import now
from .logica import obtener_configuracion

# Vista de registro de usuario
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
    else:
        form = RegistroForm()
    return render(request, 'app_memorygame/registro.html', {'form': form})

# Vista de login de usuario
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = LoginForm()
    return render(request, 'app_memorygame/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista del menú principal (después de iniciar sesión)
@login_required
def menu_view(request):
    return render(request, 'app_memorygame/menu.html')

# Vista para seleccionar el nivel y crear partida
@login_required
def seleccionar_nivel_view(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel', 'B')
        juego = iniciar_partida(request.user, nivel)
        return redirect('tablero', juego_id=juego.id)
    return redirect('menu')

# Vista para mostrar el tablero
@login_required
def tablero_view(request, juego_id):
    juego = Game.objects.get(id=juego_id, user=request.user)
    cantidad_pares, vidas = obtener_configuracion(juego.level)
    vidas_restantes = max(vidas - juego.attempts, 0)
    return render(request, 'app_memorygame/tablero.html', {
        'juego': juego,
        'vidas_restantes': vidas_restantes
    })


