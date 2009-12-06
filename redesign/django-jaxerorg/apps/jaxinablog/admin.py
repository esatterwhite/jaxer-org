from django.contrib import admin
from jaxinablog.models import RelatedContent, StandardBlogEntry, UserBlog
from django.contrib.contenttypes import generic

class RelatedContentInline(generic.GenericStackedInline):
    model = RelatedContent
    
class UserBlogAdmin(admin.ModelAdmin):
    list_display = ('owner','title')
class BlogEntryAdmin(admin.ModelAdmin):
    inlines = [RelatedContentInline,]
    
admin.site.register(RelatedContent) 
admin.site.register(UserBlog, UserBlogAdmin)
admin.site.register(StandardBlogEntry, BlogEntryAdmin)