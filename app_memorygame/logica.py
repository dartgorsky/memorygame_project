from app_memorygame.models import Game, Card, Statistic
from django.contrib.auth.models import User
from django.utils.timezone import now
import random

# --------------------------------------------------
# Función para obtener la configuración según el nivel
# Devuelve: (cantidad de pares, vidas máximas)
# --------------------------------------------------
def obtener_configuracion(nivel):
    if nivel == 'B':  # Básico
        return 8, 6
    elif nivel == 'M':  # Medio
        return 8, 4
    elif nivel == 'A':  # Avanzado
        return 8, 2
    else:
        return 8, 6  # Por defecto: básico

# --------------------------------------------------
# Inicia una partida nueva para un usuario
# Nivel por defecto: 'B' (Básico)
# --------------------------------------------------
def iniciar_partida(user, nivel='B'):
    cantidad_pares, vidas=obtener_configuracion(nivel)
    todas_las_cartas=list(Card.objects.all())

    # Selecciona cartas aleatorias sin repetir
    seleccionadas=random.sample(todas_las_cartas, cantidad_pares)

    # Duplica las cartas para hacer pares y las mezcla
    cartas_para_jugar = seleccionadas * 2
    random.shuffle(cartas_para_jugar)

    # Crea la partida con el usuario y nivel
    juego=Game.objects.create(user=user, level=nivel, max_attempts=vidas)
    juego.cards.set(cartas_para_jugar)
    juego.save()
    return juego

# --------------------------------------------------
# Verifica si dos cartas forman un par (tienen el mismo ID)
# --------------------------------------------------
def verificar_emparejamiento(carta1, carta2):
    return carta1.id==carta2.id

# --------------------------------------------------
# Registra un intento del usuario con dos cartas seleccionadas
# Suma score si hay emparejamiento
# Llama a revisar_estado_juego para validar si ganó o perdió
# --------------------------------------------------
def registrar_intento(juego, carta1, carta2):
    if juego.status != 'P':
        return  # No se puede registrar si ya ganó o perdió

    juego.attempts += 1

    if verificar_emparejamiento(carta1, carta2):
        juego.score += 1
        # Ya no guardamos "matched" porque no existe ese campo

    juego.save()
    revisar_estado_juego(juego)

# --------------------------------------------------
# Actualiza estadísticas del usuario
# --------------------------------------------------
def actualizar_estadisticas(usuario, gano, puntaje):
    estadistica, creado = Statistic.objects.get_or_create(user=usuario)
    estadistica.total_games += 1

    if gano:
        estadistica.wins += 1
    else:
        estadistica.losses += 1

    estadistica.average_score = (
        (estadistica.average_score * (estadistica.total_games - 1) + puntaje)
        / estadistica.total_games
    )
    estadistica.save()

# --------------------------------------------------
# Revisa si el usuario ganó, perdió o sigue jugando
# Aplica un bono de puntaje si gana (vidas restantes * 10)
# --------------------------------------------------
def revisar_estado_juego(juego):
    cantidad_pares, vidas= obtener_configuracion(juego.level)

    if juego.score==cantidad_pares:
        juego.status= 'W'  # Win
        juego.end_time= now()

        # Actualiza estadísticas: ganó y puntaje final
        actualizar_estadisticas(juego.user, True, juego.score)

    elif juego.attempts >= juego.max_attempts:
        juego.status= 'L'  # Lose
        juego.end_time= now()
        juego.save()

        # Actualiza estadísticas: ganó y puntaje final
        actualizar_estadisticas(juego.user, False, juego.score)
    else:
        juego.status= 'P'  # Playing
        juego.save()

    
