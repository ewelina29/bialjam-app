from django.conf.urls import url

from . import views

app_name = 'game'

urlpatterns = [
    url(r'add-game/$', views.add_new_game, name='add_game'),
    url(r'team-games/$', views.team_games, name='team_games'),
    url(r'remove-game/(?P<id>[^/]+)/$', views.remove_game, name='remove_game'),
    url(r'details/(?P<id>[^/]+)/$', views.game_details, name='game_details'),
    url(r'list/$', views.games_list, name='games_list')
]
