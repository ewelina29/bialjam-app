from django import forms
from .models import Game
from django.utils.translation import ugettext_lazy as _


class GameForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label=_(u'Name of the game'))
    url = forms.URLField(label=_(u'Url'), required=False)

    class Meta:
        model= Game
        fields = ('name', 'url')

    def __init__(self, current_user,  *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
