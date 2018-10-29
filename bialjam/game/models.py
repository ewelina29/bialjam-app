# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from award.models import Award
from team.models import Team

# === Models for Game app ===


def directory_path(instance, filename):
    return 'images/games/{0}'.format(filename)


class Game(models.Model):
    """
    The Game class defines the game's information. Each game has fields:
        1. name
        2. team - team the game belongs to
        3. year - the year when the game was developed
        4. url - url path to the game
        5. award - award the game has won
        6. description - short information about the game
        7. image - photo of the game cover
    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    url = models.URLField(null=True, blank=True, default='')
    award = models.ForeignKey(Award, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to=directory_path, blank=True, null=True)

    def __str__(self):
        return self.name
