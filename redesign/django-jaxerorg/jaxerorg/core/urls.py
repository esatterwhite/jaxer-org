from django.conf.urls.defaults import *

urlpatterns = patterns('jaxerorg.core.views',
    url(r'^editortest/$', 'editor_test', name='jaxerorg_core_edit'),
    url(r'^editor/insert/code/$', 'ajax_code_form', name='core_ajax_codeform'),   
    url(r'^searchtest/$', 'search_test', name='jaxerorg_core_search'),
    url(r'^formtest/$', 'formtest', name='jaxerorg_core_form'),              
)

