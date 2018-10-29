# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# === The models for Team app ===

def directory_path(instance, filename):
    return 'images/teams/{0}'.format(filename)


class Team (models.Model):
    """
    The Team class defines the team details. Each team has fields:

        1. name
        2. year - year when the team was taking part in the contest
        3. request_users - list of users who has written messages to the team
        4. logo - team avatar
        5. infomation - short history of the team
    """
    name = models.CharField(max_length=50, unique=True)
    year = models.PositiveSmallIntegerField()
    request_users = models.ManyToManyField(User, through="RequestUserTeam",
                                           through_fields=('team', 'user'))
    logo = models.ImageField(upload_to=directory_path, blank=True, null=True)
    information = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class RequestUserTeam(models.Model):
    """
    The RequestUserTeam class defines the message sent from user to team. Each request has fields:

        1. team - team the request was addressed to
        2. user - sender of the request
        3. message - content of the request
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.team.name + ' - ' + self.user.username
