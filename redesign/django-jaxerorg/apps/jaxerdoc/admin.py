from django.contrib import admin
from jaxerdoc.models import JavascriptObject, ClassItem, Function, JaxerNameSpace,\
Property, Parameter, FunctionalityGroup
from django.contrib.contenttypes import generic
#inline definitions
class AdminMethodInline(generic.GenericStackedInline):
    model = Function
    fieldsets = (
        (None,{'fields': ('name','editor')}),
        ('Information',{
                        'fields':('content',),
                        'classes':('collapse', )
                        }
        ),
#        ('Returns',{
#                    'fields':('return_param',('return_type','type_id')),
#                    'classes':('collapse', )
#                    }
#        ),
        ('Availability',{
                      'fields':(('availablity','is_depricated'),('client_side', 'server_side'))
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
    list_display = ('name','id')
#modeladmin definitions
class AdminJavaScriptObject(admin.ModelAdmin):
    inlines = [AdminMethodInline, AdminPropertyInline ]
    list_display = ('name', 'id')
    list_filter = ('naitive',)
    fieldsets = (
                 (None,{
                       'fields':('editor',('name','naitive'),'content')
                       }
                 ),
                 
                 ('Framework',{
                               'fields':('server_side','client_side')
                               }
                 )
                )
class AdminClassItem(admin.ModelAdmin):
    inlines = [AdminParameterInline, AdminMethodInline, AdminPropertyInline ]
    list_display = ('class_name','id')
    fieldsets = (
        (None,{
               'fields':('editor',)
               }
        ),
        ('General',
            {
             'fields':(('namespace','name'),'content'),
             }
         ),
         ('Availibility',{
                          'fields':('availablity',('is_depricated','depricated'))
                          }
         ),
         ('Framework',{
                          'fields':('client_side','server_side')
                          }
         ),
#         ('Return',
#            {
#             'fields':('return_param', ('return_type', 'type_id'),),
#             
#             }
#          )
    )
    
class AdminJaxerNameSpace(admin.ModelAdmin):
    list_display=('name', 'id')
    inlines = [AdminParameterInline, AdminMethodInline, AdminPropertyInline ]
    exclude = ['naitive']    
class AdminFunctionModel(admin.ModelAdmin):
    inlines = [AdminParameterInline, AdminJavascriptObjectInline]
    list_display= ('name',)
    fieldsets=(
        (None,{'fields': ('editor',)}),
        ('Information',{'fields':('name',('content','is_global','example_code'))}),
        ('Link To',{'fields':('content_type','object_id')}),
        ('Availability',{
                      'fields':('availablity', ('is_depricated','depricated'),('client_side', 'server_side'))
                      }
        ),
        
    )
class AdminParameterModel(admin.ModelAdmin):
    inlines = [AdminPropertyInline, ]
    list_display = ('name', 'id')
class AdminPropertyModel(admin.ModelAdmin):
    inlines = [AdminPropertyInline,]
    list_display = ('name', 'id')
    
admin.site.register(JavascriptObject, AdminJavaScriptObject)
admin.site.register(ClassItem, AdminClassItem)
admin.site.register(JaxerNameSpace, AdminJaxerNameSpace)
admin.site.register(Property, AdminPropertyModel)
admin.site.register(Function, AdminFunctionModel)
admin.site.register(Parameter, AdminParameterModel)
admin.site.register(FunctionalityGroup)
