from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .logica import iniciar_partida, obtener_configuracion, actualizar_estadisticas
from .models import Game
from django.utils.timezone import now
import random
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce, Now

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

# Selección de nivel y creación de partida
@login_required
def seleccionar_nivel_view(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel')  # 'B', 'M' o 'A'
        juego = iniciar_partida(request.user, nivel)
        return redirect('tablero', juego_id=juego.id)
    else:
        return redirect('menu')

# Vista del tablero del juego 
@login_required
def tablero_view(request, juego_id):
    juego = get_object_or_404(Game, id=juego_id, user=request.user)

    if request.method == 'POST':
        status = request.POST.get('status')  # 'W' o 'L'
        attempts = request.POST.get('attempts')
        score = request.POST.get('score')

        # Validar y convertir los datos recibidos
        try:
            attempts = int(attempts)
            score = int(score)
        except (TypeError, ValueError):
            attempts = juego.attempts
            score = juego.score

        juego.status = status if status in ['W', 'L', 'P'] else juego.status
        juego.attempts = attempts
        juego.score = score
        juego.end_time = now()
        juego.save()

        # Actualizar estadísticas si la partida terminó (W o L)
        if status in ['W', 'L']:
            gano = (status == 'W')
            actualizar_estadisticas(request.user, gano, score)

        # Preparar datos para renderizar la plantilla con resultado
        cantidad_pares, max_vidas = obtener_configuracion(juego.level)
        vidas_restantes = max(max_vidas - (juego.attempts - juego.score), 0)

        cartas_unicas = list(juego.cards.all())
        cartas_para_mostrar = cartas_unicas * 2
        random.shuffle(cartas_para_mostrar)

        return render(request, 'app_memorygame/tablero.html', {
            'juego': juego,
            'vidas_restantes': vidas_restantes,
            'cartas': cartas_para_mostrar,
            'tiempo_total': 60,
            'resultado': status,  
        })

    # GET: Mostrar el tablero para jugar
    cantidad_pares, max_vidas = obtener_configuracion(juego.level)
    vidas_restantes = max(max_vidas - juego.attempts, 0)

    cartas_unicas = list(juego.cards.all())
    cartas_para_mostrar = cartas_unicas * 2
    random.shuffle(cartas_para_mostrar)

    return render(request, 'app_memorygame/tablero.html', {
        'juego': juego,
        'vidas_restantes': vidas_restantes,
        'cartas': cartas_para_mostrar,
        'tiempo_total': 60,
        'resultado': '', 
    })

# Perfil del usuario: estadísticas y últimas partidas
@login_required
def perfil_usuario_view(request):
    user = request.user
    stats = getattr(user, 'statistics', None)
    ultimas_partidas = user.games.order_by('-start_time')[:10]

    # Formatear duración y vidas restantes por partida
    for juego in ultimas_partidas:
        total_segundos = int(juego.duration)
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        juego.duracion_formateada = f"{minutos}m {segundos}s"
        cantidad_pares, max_vidas = obtener_configuracion(juego.level)
        juego.vidas_restantes = max(max_vidas - (juego.attempts - juego.score), 0)


    # Calcular tasa de éxito solo si hay partidas
    tasa_exito = None
    if stats and stats.total_games > 0:
        tasa_exito = round((stats.wins / stats.total_games) * 100, 1)

    contexto = {
        'stats': stats,
        'ultimas_partidas': ultimas_partidas,
        'tasa_exito': tasa_exito, 
    }
    return render(request, 'app_memorygame/perfil.html', contexto)

# Ranking de mejores partidas por nivel
@login_required
def ranking_view(request):
    niveles = {
        'B': 'Básico',
        'M': 'Medio',
        'A': 'Avanzado',
    }

    ranking = {}
    for nivel_codigo, nivel_nombre in niveles.items():
        partidas_qs = (
            Game.objects
            .filter(status='W', level=nivel_codigo)
            .annotate(
                duracion_tiempo=ExpressionWrapper(
                    Coalesce('end_time', Now()) - F('start_time'),
                    output_field=DurationField()
                )
            )
            .order_by('-score', 'duracion_tiempo')[:10]
        )

        partidas = []
        for juego in partidas_qs:
            # duración en segundos para mostrar
            duracion_segundos = int(juego.duracion_tiempo.total_seconds()) if getattr(juego, 'duracion_tiempo', None) else 0
            juego.duracion_segundos = duracion_segundos
            # vidas restantes calculadas aquí
            cantidad_pares, max_vidas = obtener_configuracion(juego.level)
            juego.vidas_restantes = max(max_vidas - (juego.attempts - juego.score), 0)
            partidas.append(juego)

        ranking[nivel_nombre] = partidas

    return render(request, 'app_memorygame/ranking.html', {
        'ranking': ranking,
    })

