from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^jaxerorg/', include('jaxerorg.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),
     url(r'^$', 'jaxerorg.core.views.jaxer_home', name='jaxerorg_core_home'),                     
    url(r'^escape/$', 'jaxerorg.core.views.escape_code', name='jaxerorg_core_escapecode'),
    url(r'^accounts/login/$', 'jaxerorg.core.views.login_user', name="jaxer_login_user"),
)
urlpatterns += patterns('',
    url(r'^core/', include('jaxerorg.core.urls')),                        
)
urlpatterns += patterns('jaxerdoc.searchviews',
    url(r'^search/', 'ajax_doc_search', name='jaxerdoc_ajax_search'),
                        
)
urlpatterns += patterns('',
    url(r'^api/', include('jaxerdoc.urls')),
)