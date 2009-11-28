'''Wiki admin config'''
from django.contrib import admin
from django.contrib.contenttypes import generic
from jaxerhotsauce.models import ChangeSet, WikiPage

class InlineChangeSet(generic.GenericTabularInline):
    '''generic inline confige of the ChangeSet'''
    model = ChangeSet
    
class WikiPageAdmin(admin.ModelAdmin):
    '''Model Admin config for the WikiPage'''
    inlines = [InlineChangeSet, ]

#admin.site.register(ChangeSet)
admin.site.register(WikiPage, WikiPageAdmin)