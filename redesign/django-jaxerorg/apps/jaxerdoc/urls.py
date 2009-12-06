from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerdoc.views',
    url(r'^(?P<oslug>[-\w]+)/(?P<ctid>\d+)-(?P<objid>\d+)/$',
        'document_detail',
        name='jaxerdoc_document_detail'),
        
    url(r'^parameter/add/(?P<add_to_ct>\d+)-(?P<add_to_id>\d+)/', 
        'add_parameter_to_object',
         name="jaxerdoc_add_param_to_object"),
         
    url(r'^(?P<ctid>\d+)-(?P<objid>\d+)/edit/$', 
        'ajax_document_edit',
         name="jaxerdoc_modify_document"),  
    url(r'^(?P<obj_id>\d+)/$', 
        'diff_test',
         name="difference_text"),                
)

urlpatterns += patterns('jaxerdoc.extraviews.moderate',
    url(r'^queue/moderate/list/(?P<filter>\w+)/$', 'queue_manager', name="jaxerdoc_queue_moderation_filter"),
    url(r'^queue/moderate/list/$', 'queue_manager', name="jaxerdoc_queue_moderation"),
    url(r'^queue/moderate/(?P<queue_id>\d+)/$', 'moderate_queue', name="jaxerdoc_moderation_preview"),
    url(r'^queue/moderate/(?P<queue_id>\d+)/difference/$', 'show_difference', name="jaxerdoc_moderation_difference"),    
)

urlpatterns += patterns('jaxerdoc.views',
    url(r'^add/parameter/', 'add_parameter_to_object', name='jaxerdoc_search_object_form')                        
)