from django import forms
from .models import Team, User, RequestUserTeam
from django.utils.translation import ugettext_lazy as _


def get_users(current_user):
    users = User.objects.filter(profile__team__isnull=True).exclude(pk=current_user.pk).order_by('username')
    user_choices = [(user.id, user.username) for user in users]
    user_choices.insert(0, ('', '-'))

    return user_choices


class TeamForm(forms.ModelForm):

    name = forms.CharField(max_length=50, label=_(u'Team name'))
    member1 = forms.CharField(max_length=50, disabled=True, label=_(u'Member 1'))
    member2 = forms.ChoiceField(required=False, label=_(u'Member 2'))
    member3 = forms.ChoiceField(required=False, label=_(u'Member 3'))
    member4 = forms.ChoiceField(required=False, label=_(u'Member 4'))

    def __init__(self, current_user,  *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        if current_user is not None:
            self.fields['member1'].initial = current_user.username
            self.fields['member2'].choices = get_users(current_user)
            self.fields['member3'].choices = get_users(current_user)
            self.fields['member4'].choices = get_users(current_user)

    class Meta:
        model = Team
        fields = ('name',)

    def clean(self):
        cleaned_data = super(TeamForm, self).clean()
        name = cleaned_data.get('name')
        member2 = cleaned_data.get('member2')
        member3 = cleaned_data.get('member3')
        member4 = cleaned_data.get('member4')

        if not name:
            self._errors['name'] = _('Name is required')

        if member3 == member2 and member3 != '':
            self._errors['member3'] = _('You cannot choose the same member twice')

        if member4 == member2 and member4 != '':
            self._errors['member4'] = _('You cannot choose the same member twice')

        if member4 == member3 and member4 != '':
            self._errors['member4'] = _('You cannot choose the same member twice')

        return cleaned_data


#User see all teams and may choose few teams and send resuest to add him to team
class UserRequestForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects, label=_(u'Teams'))
    message = forms.CharField(widget=forms.Textarea, max_length=250, label=_(u'Message'))

    class Meta:
        model = RequestUserTeam
        fields = ('message',)

# class TeamFormDetails(forms.ModelForm):
#
#     members = forms.Mo
#
#     class Meta:
#         model = Team
#         fields = ('name', )
