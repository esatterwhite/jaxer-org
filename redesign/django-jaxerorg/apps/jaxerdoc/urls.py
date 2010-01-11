from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerdoc.views',
                       
    url(r'^$','docs_root',name='jaxerdoc_docs_home'),
    url(r'^(?P<oslug>[-\w]+)/(?P<ctid>\d+)-(?P<objid>\d+)/$',
        'document_detail',
        name='jaxerdoc_document_detail'),
        
         
    url(r'^(?P<ctid>\d+)-(?P<objid>\d+)/edit/$', 
        'ajax_document_edit',
         name="jaxerdoc_modify_document"),  
    url(r'^(?P<obj_id>\d+)/$', 
        'diff_test',
         name="difference_text"),                
)
urlpatterns += patterns('jaxerdoc.wiki_views.create_object',
    url(r'^parameter/add/(?P<add_to_ct_id>\d+)-(?P<add_to_id>\d+)/', 
        'add_parameter_to_object',
         name="jaxerdoc_add_param_to_object"),
)

urlpatterns += patterns('jaxerdoc.wiki_views.moderate',
    url(r'^queue/moderate/list/(?P<filter>\w+)/$', 'queue_manager', name="jaxerdoc_queue_moderation_filter"),
    url(r'^queue/moderate/list/$', 'queue_manager', name="jaxerdoc_queue_moderation"),
    url(r'^queue/moderate/(?P<queue_id>\d+)/$', 'moderate_queue', name="jaxerdoc_moderation_preview"),
    url(r'^queue/moderate/(?P<queue_id>\d+)/difference/$', 'show_difference', name="jaxerdoc_moderation_difference"),
    url(r'^queue/moderate/proposal/(?P<queue_id>\d+)/$', 'moderate_new_object', name='jaxerdoc_moderate_new_object'),    
)

urlpatterns += patterns('jaxerdoc.wiki_views.create_object',
    url(r'^add/(?P<add_ct_id>\d+)/(?P<ct_id>\d+)-(?P<obj_id>\d+)/$', 'add_object_proposal', name="jaxerdoc_propose_linked_object"),
    url(r'^add/class/(?P<add_to_ct_id>\d+)/(?P<add_to_id>\d+)/$', 'add_class_to_object', name="jaxerdoc_add_class_to_object"),
    
)

