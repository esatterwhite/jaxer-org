''' hotsauce urls'''

from django.conf.urls.defaults import *

urlpatterns = patterns('hotsauce.views',
    url(r'^$','wiki_list',name='hotsauce_list'),
    url(r'^wikimode/$','add_edit_item', name='hotsauce_wiki_new'),
    url(r'^(?P<item>[-\w]+)/(?P<obj_id>\d+)/wikimode/$','add_edit_item', name='hotsauce_wiki_edit'),
    url(r'^(?P<item>[-\w]+)/changeset/(?P<obj_id>\d+)/$','view_changes', name='hotsauce_change_view')
)