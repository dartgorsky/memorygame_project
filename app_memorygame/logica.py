from app_memorygame.models import Game, Card
from django.contrib.auth.models import User
from django.utils.timezone import now
import random

def iniciar_partida(user):
    game = Game.objects.create(user=user)
    cartas = list(Card.objects.all())
    seleccionadas = random.sample(cartas, 6)  
    cartas_emparejadas = seleccionadas * 2
    random.shuffle(cartas_emparejadas)
    game.cards.set(cartas_emparejadas)
    game.save()
    return game

def verificar_emparejamiento(carta1: Card, carta2: Card) -> bool:
    return carta1.id == carta2.id

def registrar_intento(game: Game, carta1: Card, carta2: Card):
    game.attempts += 1
    if verificar_emparejamiento(carta1, carta2):
        game.score += 1  
    game.save()

def revisar_estado_juego(game: Game):
    total_pares = game.cards.count() // 2
    if game.score == total_pares:
        game.status = 'W'
        game.end_time = now()
    elif game.attempts >= total_pares * 3:  
        game.status = 'L'
        game.end_time = now()
    game.save()


