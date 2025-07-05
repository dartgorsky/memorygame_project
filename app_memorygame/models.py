from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    # Información de la carta
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    value = models.IntegerField()

    def __str__(self):
        return self.name

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    
    # Si querés guardar qué cartas se usaron en esta partida:
    cards = models.ManyToManyField(Card, blank=True)

    def __str__(self):
        return f"Game #{self.id} - User: {self.user.username}"