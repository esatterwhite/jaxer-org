'''jaxerorg core admin configuration'''
from django.contrib import admin
from jaxerorg.core.models import JaxerRelease, JaxerDownload, HomePageItem, HomeScrollPaneItem
from django.contrib.contenttypes import generic

class JaxerDownloadInline(generic.GenericStackedInline):
    model = JaxerDownload
    
    
class AdminJaxerRelease(admin.ModelAdmin):
    inlines = [JaxerDownloadInline,]
    fieldsets = (
        (None,
            {'fields':('name',)}),
        ('Version',{'fields':(('major','minor','security','bug_fix'),'development')}),
        ('Extra Info',{'fields':('notes',)})
        
    )
admin.site.register(JaxerRelease, AdminJaxerRelease)
admin.site.register(HomePageItem)
admin.site.register(HomeScrollPaneItem)