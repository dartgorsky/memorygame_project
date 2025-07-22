from app_memorygame.models import Game, Card
from django.contrib.auth.models import User
from django.utils.timezone import now
import random

# --------------------------------------------------
# Función para obtener la configuración según el nivel
# Devuelve: (cantidad de pares, vidas máximas)
# --------------------------------------------------
def obtener_configuracion(nivel):
    if nivel=='B':  # Nivel Básico
        return 6, 10
    elif nivel=='M':  # Nivel Medio
        return 8, 5
    elif nivel=='A':  # Nivel Avanzado
        return 10, 3
    else:  # Valor por defecto
        return 6, 10

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
    cartas_para_jugar=seleccionadas*2
    random.shuffle(cartas_para_jugar)

    # Crea la partida con el usuario y nivel
    juego=Game.objects.create(user=user, level=nivel)
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
    juego.attempts+= 1

    if verificar_emparejamiento(carta1, carta2):
        juego.score+= 1
        carta1.matched= True
        carta2.matched= True
        carta1.save()
        carta2.save()

    juego.save()
    revisar_estado_juego(juego)

# --------------------------------------------------
# Revisa si el usuario ganó, perdió o sigue jugando
# Aplica un bono de puntaje si gana (vidas restantes * 10)
# --------------------------------------------------
def revisar_estado_juego(juego):
    cantidad_pares, vidas= obtener_configuracion(juego.level)

    if juego.score==cantidad_pares:
        juego.status= 'W'  # Win
        juego.end_time= now()

        # Bono adicional por vidas restantes
        vidas_restantes=max(vidas-juego.attempts, 0)
        juego.score+= vidas_restantes*10

    elif juego.attempts>= vidas:
        juego.status= 'L'  # Lose
        juego.end_time= now()
    else:
        juego.status= 'P'  # Playing

    juego.save()
