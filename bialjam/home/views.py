# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from information.models import Information

# === Views for Home app ===

"""
 Home app includes the following views:

 1. **Home** - Return home view and calculate the days remaining to contest.  (jump to section in [[views.py#home]] )
 """


# === home ===
def home(request):
    template = loader.get_template('home/home.html')
    context = {
        'days': Information.getDaysToContest()
    }
    return HttpResponse(template.render(context, request))
