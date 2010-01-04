'''Wiki admin config'''
from django.contrib import admin
from django.contrib.contenttypes import generic
from jaxerhotsauce.models import ChangeSet

class InlineChangeSet(generic.GenericTabularInline):
    '''generic inline confige of the ChangeSet'''
    model = ChangeSet


#admin.site.register(ChangeSet)
