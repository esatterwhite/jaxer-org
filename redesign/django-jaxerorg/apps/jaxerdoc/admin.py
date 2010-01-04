from django.contrib import admin
from jaxerdoc.models import JavascriptObject, ClassItem, Function, JaxerNameSpace, \
Property, Parameter, FunctionalityGroup
from django.contrib.contenttypes import generic
#inline definitions
class AdminMethodInline(generic.GenericStackedInline):
    model = Function
    fieldsets = (
        (None, {'fields': ('name', 'editor')}),
        ('Information', {
                        'fields':('content',),
                        'classes':('collapse',)
                        }
        ),
#        ('Returns',{
#                    'fields':('return_param',('return_type','type_id')),
#                    'classes':('collapse', )
#                    }
#        ),
        ('Availability', {
                      'fields':(('availablity', 'is_depricated'), ('client_side', 'server_side'))
                      }
        ),
    )

class AdminParameterInline(generic.GenericStackedInline):
    model = Parameter

class AdminPropertyInline(generic.GenericStackedInline):

    model = Property
    list_display = ('content_type', 'object_id')    
class AdminJavascriptObjectInline(generic.GenericStackedInline):
    inlines = [AdminMethodInline, AdminPropertyInline]
    model = JavascriptObject
    verbose_name = "Object Returned"
    list_display = ('name', 'id')
#modeladmin definitions
class AdminJavaScriptObject(admin.ModelAdmin):
    inlines = [AdminMethodInline, AdminPropertyInline ]
    list_display = ('name', 'id')
    list_filter = ('naitive','editor')
    fieldsets = (
                 (None, {
                       'fields':('editor', ('name', 'naitive'), 'content')
                       }
                 ),
                 
                 ('Server Model', {
                               'fields':('server_side', 'client_side')
                               }
                 )
                )
class AdminClassItem(admin.ModelAdmin):
#    inlines = [AdminParameterInline, AdminMethodInline, AdminPropertyInline ]
    list_display = ('class_name', 'id')
    filter_horizontal = ('properties', 'methods', 'parameters')
    list_filter = ('editor',)
    related_search_fields={
        'editor':('last_name','first_name'),
    }
    fieldsets = (
        (None, {
               'fields':('editor',)
               }
        ),
        ('General',
            {
             'fields':(('namespace', 'name'), 'content', 'properties', 'methods', 'parameters'),
             }
         ),
         ('Availibility', {
                          'fields':('availablity', ('is_depricated', 'depricated'))
                          }
         ),
         ('Framework', {
                          'fields':('client_side', 'server_side')
                          }
         ),

    )
    
class AdminJaxerNameSpace(admin.ModelAdmin):
    list_display = ('name', 'id')
#    inlines = [AdminParameterInline, AdminMethodInline, AdminPropertyInline ]
    filter_horizontal = ('methods', 'properties')
    search_fields = ['^editor__username', 'name']
    fieldsets=(
        (None, {'fields':('editor',('name', 'category'), 'on_line','content')}),
        ('Server Model', {'fields':(('server_side', 'client_side'),)}),
        ('Inheritance', {'fields':(('root_namespace','parent_namespace'),('methods','properties'))}),
        ('Availability',{'fields':('availablity',('is_depricated', 'depricated'))}),      
    )    
class AdminFunctionModel(admin.ModelAdmin):
    inlines = [AdminJavascriptObjectInline,]
    list_display = ('name',)
    search_fields = ['^editor__username','name']
    fieldsets = (
        (None, {'fields': ('editor',)}),
        ('Information', {'fields':('name', ('content', 'is_global', 'example_code'))}),
        #('Returns', {'fields':('return_param', 'return_type', 'type_id')}),
        ('Availability', {
                      'fields':('availablity', ('is_depricated', 'depricated'), ('client_side', 'server_side'))
                      }
        ),
        ('parameters',{
                       'fields':('parameters',)
                       }
        ),
        
    )
class AdminParameterModel(admin.ModelAdmin):
#    inlines = [AdminPropertyInline, ]
    list_display = ('name', 'id')
class AdminPropertyModel(admin.ModelAdmin):
#    inlines = [AdminPropertyInline, ]
    list_display = ('name', 'id')
    
admin.site.register(JavascriptObject, AdminJavaScriptObject)
admin.site.register(ClassItem, AdminClassItem)
admin.site.register(JaxerNameSpace, AdminJaxerNameSpace)
admin.site.register(Property, AdminPropertyModel)
admin.site.register(Function, AdminFunctionModel)
admin.site.register(Parameter, AdminParameterModel)
admin.site.register(FunctionalityGroup)
