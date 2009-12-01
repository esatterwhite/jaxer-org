from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerdoc.views',
    url(r'^(?P<oslug>[-\w]+)/(?P<ctid>\d+)-(?P<objid>\d+)/$',
        'document_detail',
        name='jaxerdoc_document_detail'),
        
    url(r'^parameter/add/(?P<add_to_ct>\d+)-(?P<add_to_id>\d+)/', 
        'add_parameter_to_object',
         name="jaxerdoc_add_param_to_object"),
)



urlpatterns += patterns('jaxerdoc.views',
    url(r'^add/parameter/', 'add_parameter_to_object', name='jaxerdoc_search_object_form')                        
)