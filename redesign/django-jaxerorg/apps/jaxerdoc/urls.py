from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerdoc.views',
    url(r'(?P<oslug>[-\w]+)/(?P<ctid>\d+)-(?P<objid>\d+)/$',
        'document_detail',
        name='jaxerdoc_document_detail')
)