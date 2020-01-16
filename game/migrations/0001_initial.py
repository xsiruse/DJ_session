# Generated by Django 2.1.1 on 2020-01-14 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guessed_number', models.IntegerField(verbose_name='Загаданное число')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggested_number', models.IntegerField(verbose_name='Предложенное число')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_host', models.BooleanField(default=False, verbose_name='Ведущий')),
                ('gameplay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_rel', to='game.Game')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_rel', to='game.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='player',
            field=models.ManyToManyField(related_name='player', through='game.PlayerGameInfo', to='game.Player'),
        ),
    ]
