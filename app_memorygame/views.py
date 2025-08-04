from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm
from .logica import iniciar_partida
from .models import Game, Card
from django.utils.timezone import now
from .logica import registrar_intento, obtener_configuracion, actualizar_estadisticas
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

@login_required
def seleccionar_nivel_view(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel')  # 'B', 'M' o 'A'
        juego = iniciar_partida(request.user, nivel)
        return redirect('tablero', juego_id=juego.id)
    else:
        return redirect('menu')

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
        vidas_restantes = max(max_vidas - juego.attempts, 0)

        cartas_unicas = list(juego.cards.all())
        cartas_para_mostrar = cartas_unicas * 2
        random.shuffle(cartas_para_mostrar)

        tiempos_por_nivel = {'B': 120, 'M': 240, 'A': 300}
        tiempo_total = tiempos_por_nivel.get(juego.level, 120)

        return render(request, 'app_memorygame/tablero.html', {
            'juego': juego,
            'vidas_restantes': vidas_restantes,
            'cartas': cartas_para_mostrar,
            'tiempo_total': tiempo_total,
            'resultado': status,  # Para mostrar modal en JS
        })

    # GET: Mostrar el tablero para jugar
    cantidad_pares, max_vidas = obtener_configuracion(juego.level)
    vidas_restantes = max(max_vidas - juego.attempts, 0)

    cartas_unicas = list(juego.cards.all())
    cartas_para_mostrar = cartas_unicas * 2
    random.shuffle(cartas_para_mostrar)

    tiempos_por_nivel = {'B': 120, 'M': 240, 'A': 300}
    tiempo_total = tiempos_por_nivel.get(juego.level, 120)

    return render(request, 'app_memorygame/tablero.html', {
        'juego': juego,
        'vidas_restantes': vidas_restantes,
        'cartas': cartas_para_mostrar,
        'tiempo_total': tiempo_total,
        'resultado': '',  # No hay resultado aún
    })

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
        juego.vidas_restantes = max(juego.max_attempts - juego.attempts, 0)

    # Calcular tasa de éxito solo si hay partidas
    tasa_exito = None
    if stats and stats.total_games > 0:
        tasa_exito = round((stats.wins / stats.total_games) * 100, 1)

    contexto = {
        'stats': stats,
        'ultimas_partidas': ultimas_partidas,
        'tasa_exito': tasa_exito,  # Enviamos la tasa ya calculada
    }
    return render(request, 'app_memorygame/perfil.html', contexto)

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
            juego.vidas_restantes = max(juego.max_attempts - juego.attempts, 0)
            partidas.append(juego)

        ranking[nivel_nombre] = partidas

    return render(request, 'app_memorygame/ranking.html', {
        'ranking': ranking,
    })

