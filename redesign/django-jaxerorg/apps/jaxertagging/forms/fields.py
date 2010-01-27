'''http://docs.python.org/library/sets.html'''
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from jaxerutils.utils import get_object
from django.db.models.fields import CharField
'''    
    This aims to be a generic input field where values are 
    OBJECT.CONTENT_TYPE_ID-OBJECT.PK seperated by commas
    i.e. 34-323,34-221,21-34,43-2342
'''
class CommaSeparatedObjectInput(widgets.Input):
    input_type = 'text'
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([obj.get_id_code() for obj in value]))
        return super(CommaSeparatedObjectInput, self).render(name, value, attrs)   
class CommaSeperatedObjectField(forms.Field):
    widget = CommaSeparatedObjectInput

