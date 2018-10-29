# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Game
from .forms import GameForm
from bialjam.core import CustomHttpResponse

# === Views for Game app ===


"""
Game app includes the following views:

 1. **Add new game** - Add new game views (jump to section in [[views.py#add_new_game]] )
 2. **User's team games** - Show list of all team games belong to auth user ( jump to section in [[views.py#team_games]] )
 3. **Remove game** - Remove game(jump to section in [[views.py#remove_game]])
 4. **Game details** - Show game details(jump to section in [[views.py#game_details]])
 5. **List of all games** - Show list of all games(jump to section in [[views.py#games_list]])
 """


# === add_new_game ===
@login_required
def add_new_game(request):
    """
    Adding new game
    """
    template = loader.get_template('game/add_game.html')

    if request.method == 'POST':
        form = GameForm(request.user, request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.year = datetime.datetime.now().year
            game.team = request.user.profile.team
            if 'game_image' in request.FILES:
                game.image = request.FILES['game_image']
            if request.POST.get('description_game'):
                game.description = request.POST.get('description_game')
            game.save()
        else:
            messages.error(request, _("Fill all fields"))
            return CustomHttpResponse.send(template, {}, request)

        return redirect('/games/team-games')
    else:
        if request.user.profile.team is None:
            return redirect('/team/new')
        form = GameForm(request.user)

    context = {'form': form}
    return CustomHttpResponse.send(template, context, request)


# === team_games ===
@login_required
def team_games(request):
    """
    Show all games, which belong to auth user
    """
    template = loader.get_template('game/team_games.html')

    team = request.user.profile.team

    if team:
        games = Game.objects.filter(team=team).order_by('name')
        paginator = Paginator(games, 6)

        page = request.GET.get('page')
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            games = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            games = paginator.page(paginator.num_pages)

        context = {
            'team_games': games,
            'team_name': team.name
        }

        return CustomHttpResponse.send(template, context, request)
    else:
        return redirect('/team/new')


# === remove_game ===
@login_required
def remove_game(request, id):
    """
    Remove game, which belong to user team
    """
    template = loader.get_template('game/remove_game.html')
    context = {}
    if request.method == 'POST':
        Game.objects.filter(pk=id).delete()
        return redirect('/games/team-games')
    else:
        try:
            game = Game.objects.get(pk=id)
        except Game.DoesNotExist:
            messages.error(request, _("This game does not exist"))
            return CustomHttpResponse.send(template, context, request)

        user_team = request.user.profile.team

        if game.team.id is not user_team.id:
            messages.error(request, _("You can't remove this game, it's not belong to your team"))

        else:
            context = {
                'game': game
            }

    return CustomHttpResponse.send(template, context, request)


# === game_details ===
def game_details(request, id):
    """
    Show game details
    """
    template = loader.get_template('game/game_details.html')
    context = {}

    try:
        game = Game.objects.get(pk=id)
    except Game.DoesNotExist:
        messages.error(request, _("This game does not exist"))
        return CustomHttpResponse.send(template, context, request)

    context = {
        'game': game
    }

    return CustomHttpResponse.send(template, context, request)


# === games_list ===
def games_list(request):
    """
    Show all games
    """
    template = loader.get_template('game/games_list.html')

    games = Game.objects.order_by('name')
    paginator = Paginator(games, 6)

    page = request.GET.get('page')
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        games = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        games = paginator.page(paginator.num_pages)

    context = {
        'games': games,
    }

    return CustomHttpResponse.send(template, context, request)
