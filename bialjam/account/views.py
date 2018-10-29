from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.template import loader
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from bialjam.core import CustomHttpResponse
from account.models import Profile
from .forms import SignUpForm, UserForm, ProfileForm

# === Views for Account app ===


"""
Account app includes the following views:


 1. **Signup** - Signup to create account (jump to section in [[views.py#signup]] )
 2. **Update profile** - Update profile( jump to section in [[views.py#update_profile]] )
 3. **Change password** - Changing password(jump to section in [[views.py#change_password]])
 4. **Remove user account** - Removing user's account(jump to section in [[views.py#remove_user]])
 5. **List of all users** - Show list of all users(jump to section in [[views.py#users_list]])
 6. **User details** - Show user details(jump to section in [[views.py#users_details]])
 """


# === signup ===
def signup(request):
    """
    Signup
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, _('Your account has been created.'))
    else:
        form = SignUpForm()

    template = loader.get_template('account/signup.html')

    context = {
        'form': form
    }
    return CustomHttpResponse.send(template, context, request)


# === update_profile ===
@login_required
@transaction.atomic
def update_profile(request):
    """
    Update profile
    """
    profile = request.user.profile
    user_avatar = profile.image

    if request.POST.get('save_avatar') and 'avatar_image' in request.FILES:
        profile.image = request.FILES['avatar_image']
        profile.save()
        user_avatar = profile.image

    if request.POST.get('save_fields'):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        else:

            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    template = loader.get_template('account/details.html')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_avatar': user_avatar,
    }
    return CustomHttpResponse.send(template, context, request)


# === change_password ===
@login_required
def change_password(request):
    """
    Changing password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/details')
    else:
        form = PasswordChangeForm(user=request.user)

    template = loader.get_template('account/change-password.html')

    context = {
        'form': form
    }
    return CustomHttpResponse.send(template, context, request)


# === remove_user ===
@login_required
def remove_user(request):
    """
    User remove his account
    """
    if request.method == 'POST':

        rem = User.objects.get(username=request.user.username)
        if rem is not None:
            rem.is_active = False
            rem.save()
            return redirect('/home')

    template = loader.get_template('account/remove-user.html')

    return CustomHttpResponse.send(template, {}, request)


# === users_list ===
def users_list(request):
    """
    Show list of all users
    """
    all_users = []
    users = User.objects.all()
    for user in users:
        profile = Profile.objects.get(user=user)
        team = ''
        location = ''
        if profile.team is not None:
            team = profile.team.name
        if profile.location is not None:
            location = profile.location

        user_info = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'team': team,
            'image': profile.image,
            'location': location
        }

        all_users.append(user_info)

    template = loader.get_template('account/users_list.html')

    context = {
        'users_list': all_users,
    }
    return CustomHttpResponse.send(template, context, request)


# === users_details ===
def users_details(request, pk):
    """
    Show user details
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        messages.error(request, 'Requested user does not exist!')
        return render(request, 'account/user_details.html', )

    profile = Profile.objects.get(user=user)
    team = ''
    location = ''
    bio = ''
    if profile.team is not None:
        team = profile.team.name
    if profile.location is not None:
        location = profile.location
    if profile.bio is not None:
        bio = profile.bio

    user = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'team': team,
        'image': profile.image,
        'location': location,
        'bio': bio
    }

    template = loader.get_template('account/user_details.html')

    context = {
        'user': user,
    }
    return CustomHttpResponse.send(template, context, request)
