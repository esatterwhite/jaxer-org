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
     #############################################################
     #        THIS IS FOR SERVING STATIC MEDIA FROM DJANGO ON
     #        A LOCAL MACHINE DO NOT USE IN PRODUCTION!!!
     #
     #        remove the url below before delopment
     ##############################################################
     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
     url(r'^$', 'jaxerorg.core.views.jaxer_home', name='jaxerorg_core_home'),                     
     url(r'^escape/$', 'jaxerorg.core.views.escape_code', name='jaxerorg_core_escapecode'),
     url(r'^accounts/login/$', 'jaxerorg.core.views.login_user', name="jaxer_login_user"),
     url(r'^accounts/logout/$','jaxerorg.core.views.logout_user', name='jaxer_logout_user'),
     url(r'^mail/compose/$','jaxerorg.core.views.multi_mail', name='jaxer_multiuser_mail_compose')
     
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
urlpatterns += patterns('',
    url(r'^messages/', include('messages.urls')),
)
urlpatterns += patterns('',
    url(r'^notification/', include('notification.urls')),
)
urlpatterns += patterns('',
    url(r'^profiles/', include('jaxerprofile.urls')),                        
)
