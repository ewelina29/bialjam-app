from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Profile


class SignUpForm(UserCreationForm):
    #    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    location = forms.CharField(max_length=30, required=False, label=_(u'Location'))
    bio = forms.CharField(max_length=500, required=False, label=_(u'Bio'))

    class Meta:
        model = Profile
        fields = ('location', 'bio')


class RemoveUser(forms.Form):
    username = forms.CharField()
