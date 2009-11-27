from django import forms
from django.forms import fields
from jaxerdoc.models import ClassItem,Property, Parameter, Function, JavascriptObject, JaxerNameSpace, JaxerRelease
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from jaxerdoc.widgets import AjaxObjectSearchbar
class AddParameterForm(forms.ModelForm):
    param_type =   forms.CharField(widget=AjaxObjectSearchbar())
    editor =       forms.ModelChoiceField(User.objects.all(), widget=fields.HiddenInput())
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    
    class Meta:
        model = Parameter
