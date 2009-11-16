from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
def splitstring(value, arg, splitter="."):
    return value.split(splitter)[arg]