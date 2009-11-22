from django.contrib import admin
from jaxerdoc.models import JavascriptObject, ClassItem, Function, JaxerNameSpace, Property, Parameter
from django.contrib.contenttypes import generic
#inline definitions
class AdminMethodInline(generic.GenericStackedInline):
    model = Function
    fieldsets=(
        (None,{'fields': ('name',)}),
        ('Information',{
                        'fields':('content',),
                        'classes':('collapse', )
                        }
        ),
        ('Returns',{
                    'fields':('return_param',('return_type','type_id')),
                    'classes':('collapse', )
                    }
        ),
        ('Availability',{
                      'fields':('is_depricated',('client_side', 'server_side'))
                      }
        ),
    )
class AdminPropertyInline(generic.GenericStackedInline):
    model = Property
    list_display = ('content_type', 'object_id')
class AdminParameterInline(generic.GenericStackedInline):
    model = Parameter

#modeladmin definitions
class AdminJavaScriptObject(admin.ModelAdmin):
    inlines = [AdminMethodInline, AdminPropertyInline ]
    list_display = ('name', 'id')
    
class AdminClassItem(admin.ModelAdmin):
    inlines = [AdminParameterInline, AdminMethodInline, AdminPropertyInline ]
    list_display = ('class_name','id')
    fieldsets=(
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
         ('Return',
            {
             'fields':('return_param', ('return_type', 'type_id'),),
             
             }
          )
    )
    
class AdminJaxerNameSpace(admin.ModelAdmin):
    exclude = ['naitive']    
class AdminFunctionModel(admin.ModelAdmin):
    list_display= ('name', 'return_param')
    fieldsets=(
        (None,{'fields': ('name',)}),
        ('Information',{'fields':('content','is_global')}),
        ('Returns',{'fields':('return_param',('return_type','type_id'))}),
    )
class AdminParameterModel(admin.ModelAdmin):
    inlines = [ AdminPropertyInline ]
    
admin.site.register(JavascriptObject, AdminJavaScriptObject)
admin.site.register(ClassItem, AdminClassItem)
admin.site.register(JaxerNameSpace, AdminJaxerNameSpace)
admin.site.register(Property)
admin.site.register(Function, AdminFunctionModel)
admin.site.register(Parameter)
