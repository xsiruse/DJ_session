from django.shortcuts import render, redirect
from django.utils.crypto import random
from django.views.generic import FormView

from game.models import Game, Player, PlayerGameInfo
from game.forms import GameFormPost


def show_home(request):
    number = random.randint(0, 10)
    ids_generated = random.randint(0, 1000)

    if request.session.get('player_id') and request.session.get('game_id'):
        cur_game = Game.objects.get(game_id=request.session.get('game_id'))
        if cur_game.is_finished:
            if Game.objects.filter(is_finished=False).count() == 0:
                new_game = Game.objects.create(game_id=f'g{ids_generated}', is_finished=False, guessed_number=number)
                cur_player = Player.objects.get(player_id=request.session.get('player_id'))
                new_game.player_set = cur_player
                PlayerGameInfoAdd(new_game, cur_player, 0, True, True)
                request.session['game_id'] = f'g{ids_generated}'
                return redirect('/')
            else:
                cur_game = Game.objects.get(is_finished=False)
                cur_player = Player.objects.get(player_id=request.session.get('player_id'))
                cur_game.player_set = cur_player
                PlayerGameInfoAdd(cur_game, cur_player, 0, False, False)
                request.session['game_id'] = cur_game.game_id
                return redirect('/')
        else:
            cur_player = Player.objects.get(player_id=request.session.get('player_id'))
            if PlayerGameInfo.objects.all().filter(gameplay=cur_game).get(participant=cur_player).game_host:
                return redirect('/game-creator')
            else:
                return redirect('/gameplay')
    else:
        if Game.objects.filter(is_finished=False).count() == 0:
            new_game = Game.objects.create(game_id=f'g{ids_generated}', guessed_number=number, is_finished=False)
            new_player = Player.objects.create(player_id=f'p{ids_generated}')
            new_game.player_set = new_player
            PlayerGameInfoAdd(new_game, new_player, 0, True, True)
            request.session['player_id'] = f'p{ids_generated}'
            request.session['game_id'] = f'g{ids_generated}'
            return redirect('/')
        else:
            cur_game = Game.objects.get(is_finished=False)
            new_player = Player.objects.create(player_id=f'p{ids_generated}')
            cur_game.player_set = new_player
            PlayerGameInfoAdd(cur_game, new_player, 0, False, False)
            request.session['player_id'] = f'p{ids_generated}'
            request.session['game_id'] = cur_game.game_id
            return redirect('/')


#
# class GameplayView(FormView):
#     form = GameFormPost()


def show_gameplay(request):
    cur_game = Game.objects.get(game_id=request.session.get('game_id'))
    cur_player = Player.objects.get(player_id=request.session.get('player_id'))
    counter = PlayerGameInfo.objects.filter(gameplay=cur_game).get(participant=cur_player)
    # r = request.POST
    # form = GameplayView()
    form = GameFormPost(request.POST or None)
    context = {}

    if form.is_valid():
        # print(request.POST.get('guessed_number'))
        # print(type(request.POST.get('guessed_number')))
        answer = int(request.POST.get('guessed_number'))
        if answer == cur_game.guessed_number:
            counter.game_finished = True
            context['text'] = 'Вы угадали число!'
            context['game_over'] = True
        elif answer < cur_game.guessed_number:
            context['text'] = f'Загаданное число больше числа {answer}'
        elif answer > cur_game.guessed_number:
            context['text'] = f'Загаданное число меньше числа {answer}'
        counter.try_count += 1
        counter.save()
        context['form'] = form
        return render(request, 'gameplay.html', {'form': form, 'context': context, })
    else:
        context['form'] = form
        return render(request, 'gameplay.html', {'form': form, 'context': context, })


def show_game_creator(request):
    cur_game = Game.objects.get(game_id=request.session.get('game_id'))
    cur_player = Player.objects.get(player_id=request.session.get('player_id'))
    context = {}

    players_finished_game = PlayerGameInfo.objects \
        .filter(gameplay=cur_game) \
        .exclude(participant=cur_player) \
        .filter(game_finished=True)

    if players_finished_game:
        context['players_win'] = players_finished_game

    finished_players = PlayerGameInfo.objects.filter(gameplay=cur_game).filter(game_finished=True).count()
    all_players = PlayerGameInfo.objects.filter(gameplay=cur_game).count()

    if all_players == finished_players != 1:
        context['game_over'] = True
        cur_game.is_finished = True
        cur_game.save()

    context['number'] = cur_game.guessed_number
    return render(
        request,
        'game_creator.html',
        {'context': context}
    )


def PlayerGameInfoAdd(game, player, count, created, finished):
    PlayerGameInfo.objects.create(
        gameplay=game,
        participant=player,
        try_count=count,
        game_host=created,
        game_finished=finished
    )
