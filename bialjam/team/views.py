# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from bialjam.core import CustomHttpResponse
from information.models import Information
from team.models import Team, RequestUserTeam
from .forms import TeamForm, UserRequestForm

# === Views for the Team app ===

"""
 Team app includes the following views:

 1. **Create new team** - Create new team  (jump to section in [[views.py#new_team]] )
 2. **Team details** - Show chosen team details  (jump to section in [[views.py#team_details]] )
 2. **User's team details** - Show and edit user's team details.  (jump to section in [[views.py#my_team]] )
 2. **Join to team** - Send message for chosen team with request to join  (jump to section in [[views.py#join_team]] )
 2. **User request messages** - Return all user's requests to join user team with options  (jump to section in [[views.py#request_user]] )
 2. **Team list** - Show sorted list of all teams  (jump to section in [[views.py#team_list]] )
 """

# === new_team ===
@login_required
def new(request):
    """
    Create new team, it's possible to create one team with 4 members
    """
    template = loader.get_template('team/new.html')

    if request.method == 'POST':
        form = TeamForm(request.user, request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.year = datetime.datetime.now().year
            if 'logo_image' in request.FILES:
                team.logo = request.FILES['logo_image']
            if request.POST.get('team_info'):
                team.information = request.POST.get('team_info')
            team.save()

            # assign team to all members
            request.user.profile.team = team
            request.user.save()
            if form.cleaned_data['member2'] is not '':
                member2 = User.objects.get(pk=form.cleaned_data['member2'])
                member2.profile.team = team
                member2.save()
            if form.cleaned_data['member3'] is not '':
                member3 = User.objects.get(pk=form.cleaned_data['member3'])
                member3.profile.team = team
                member3.save()
            if form.cleaned_data['member4'] is not '':
                member4 = User.objects.get(pk=form.cleaned_data['member4'])
                member4.profile.team = team
                member4.save()

            messages.success(request, _('Your team has been created.'))

    else:
        if request.user.profile.team is not None:
            return redirect('/team/my-team')
        form = TeamForm(request.user)

    context = {'form': form}
    return CustomHttpResponse.send(template, context, request)


# === team_details ===
def team_details(request, id):
    """
     Show chosen team details
    """
    template = loader.get_template('team/details.html')

    try:
        team = Team.objects.get(pk=id)
        team_members = User.objects.filter(profile__team=team)

        context = {
            'team_name': team.name,
            'team_info': team.information,
            'team_logo': team.logo,
            'team_members': team_members,
            'days': Information.getDaysToContest()
        }

    except Team.DoesNotExist:
        context = None

    return CustomHttpResponse.send(template, context, request)


# === my_team ===
@login_required
def my_team(request):
    """
     Show and edit user's team details with ability to leave the team
    """
    template = loader.get_template('team/my_team.html')
    team = request.user.profile.team

    if team is not None:
        team_members = User.objects.filter(profile__team=team)

        context = {
            'team_name': team.name,
            'team_members': team_members,
            'team_logo': team.logo,
            'team_info': team.information
        }
        if request.POST.get('save'):
                    if request.POST.get('new_name') != '':
                        new_name = request.POST.get('new_name')
                        team.name = new_name
                    if 'logo_image' in request.FILES:
                        team.logo = request.FILES['logo_image']
                    new_info = request.POST.get('new_info')
                    team.information = new_info
                    team.save()

                    context['team_name'] = team.name
                    context['team_info'] = team.information
                    context['team_logo'] = team.logo

        if request.POST.get('save_name'):
            new_name = request.POST.get('new_name')
            team.name = new_name
            team.save()
            context['team_name'] = team.name

        if request.POST.get('save_info'):
            new_info = request.POST.get('new_info')
            team.information = new_info
            team.save()
            context['team_info'] = team.information

        if request.POST.get('save_logo'):
            team.logo = request.FILES['logo_image']
            team.save()
            context['team_logo'] = team.logo

        if request.POST.get('leave_team'):
            request.user.profile.team = None
            request.user.profile.save()
            context = None
            return redirect('/')

        return CustomHttpResponse.send(template, context, request)

    else:
        return redirect('/team/new')


# === join_team ===
@login_required
def join_team(request):
    """
    Send message for chosen team with request to join
    """
    template = loader.get_template('team/join_team.html')
    if request.method == 'POST':
        form = UserRequestForm(request.POST)
        user = request.user

        if form.is_valid():
            for team in form.cleaned_data['teams']:
                request_user_team_obj = RequestUserTeam(team=team, user=user, message=request.POST.get('message'))
                request_user_team_obj.save()
            messages.success(request, _('Your requests have been sent.'))
    else:
        team = request.user.profile.team
        if team is None:
            form = UserRequestForm()
        else:
            return redirect('/')  # User which has a team can not see this template

    context = {'form': form}
    return CustomHttpResponse.send(template, context, request)


# === request_user ===
@login_required
def request_user(request):
    """
    Return all user's requests to join user team with ability to add or remove request
    """
    template = loader.get_template('team/request_user.html')
    team = request.user.profile.team

    if team is not None:
        team_name = team.name
        request_users = RequestUserTeam.objects.filter(team=team)
        context = {
            'team_name': team_name,
            'request_users': request_users
        }

        if request.POST.get("add"):
            # Check quantity of users in team
            team_members = User.objects.filter(profile__team=team)
            if len(team_members) == 4:
                context['info'] = 'You have full team'
                return CustomHttpResponse.send(template, context, request)

            # Add user
            user_username = request.POST.get("add")
            new_member = User.objects.get(username=user_username)
            new_member.profile.team = team
            new_member.save()
            Team.request_users.through.objects.filter(user_id=new_member.id).delete()
            messages.success(request, _('User has been added.'))

        if request.POST.get("remove"):
            user_username = request.POST.get("remove")
            member = User.objects.get(username=user_username)
            Team.request_users.through.objects.filter(user_id=member.id).delete()

        return CustomHttpResponse.send(template, context, request)

    else:
        return CustomHttpResponse.send(template, None, request)


# === team_list ===
def team_list(request):
    """
     Show sorted list of all teams
    """
    template = loader.get_template('team/team_list.html')
    teams_list = Team.objects.all().order_by('name')

    if not request.user.is_authenticated:
        team = None
    else:
        team = request.user.profile.team

    paginator = Paginator(teams_list, 6)

    page = request.GET.get('page')
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        teams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        teams = paginator.page(paginator.num_pages)

    context = {
        'teams': teams,
        'team': team
    }

    return CustomHttpResponse.send(template, context, request)
