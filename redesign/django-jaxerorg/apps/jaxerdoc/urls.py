from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerdoc.views',
    url(r'(?P<oslug>[-\w]+)/(?P<ctid>\d+)-(?P<objid>\d+)/$',
        'document_detail',
        name='jaxerdoc_document_detail'),
)

urlpatterns += patterns('jaxerdoc.views',
    url(r'search/objects/', 'add_parameter_to_object', name='jaxerdoc_search_object_form')                        
)