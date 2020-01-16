from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=255, verbose_name='ИД игрока')

    def __str__(self):
        return self.player_id


class Game(models.Model):
    game_id = models.CharField(max_length=100, verbose_name='ИД Игры')
    guessed_number = models.IntegerField(verbose_name='Загаданное число')
    player = models.ManyToManyField(Player, through='PlayerGameInfo', related_name='game')  #
    is_finished = models.BooleanField(verbose_name='Игра завершена', default=False)

    def __str__(self):
        return self.game_id


class PlayerGameInfo(models.Model):
    participant = models.ForeignKey(Player, related_name='player_rel', on_delete=models.CASCADE)
    gameplay = models.ForeignKey(Game, related_name='game_rel', on_delete=models.CASCADE)
    game_host = models.BooleanField(verbose_name='Ведущий', default=False)
    try_count = models.IntegerField(verbose_name='Попытки', default=0)
    game_finished = models.BooleanField(verbose_name='Завершил игру', default=0)