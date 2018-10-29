# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# === Models for Award app ===


class Award(models.Model):
    """
        The Award defines the awards for games.

    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name