from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerprofile.views',
   url(r'search/$', 'ajax_member_search', name='jaxerprofile_ajax_member_search'),
)