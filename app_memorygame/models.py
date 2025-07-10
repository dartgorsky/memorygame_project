from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Card(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    value = models.IntegerField()

    def __str__(self):
        return self.name

class Game(models.Model):
    STATUS_CHOICES = [
        ('W', 'Win'),
        ('L', 'Lose'),
        ('P', 'Playing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    cards = models.ManyToManyField(Card, blank=True)

    def __str__(self):
        return f"Game #{self.id} - User: {self.user.username}"

    @property
    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (now() - self.start_time).total_seconds()

class Statistic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    total_games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"Statistics for {self.user.username}"
