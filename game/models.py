from django.db import models


class Player(models.Model):
    suggested_number = models.IntegerField(max_length=5, verbose_name='Предложенное число')


class Game(models.Model):
    guessed_number = models.IntegerField(max_length=5, verbose_name='Загаданное число')
    player = models.ManyToManyField(Player, through='Relationship', related_name='player')


class PlayerGameInfo(models.Model):
    participant = models.ForeignKey(Player, related_name='player_rel', on_delete=models.CASCADE)
    gameplay = models.ForeignKey(Game, related_name='game_rel', on_delete=models.CASCADE)
    game_host = models.BooleanField(verbose_name='Ведущий', default=False)
