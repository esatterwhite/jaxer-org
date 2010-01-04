from messages.forms import ComposeForm, CommaSeparatedUserField
from django.utils.translation import ugettext_lazy as _
from django import forms
class MultiUserComposeForm(ComposeForm):
    #for ajax usse
     search = forms.CharField(widget=forms.TextInput(attrs={'class':'small-input'}))
    