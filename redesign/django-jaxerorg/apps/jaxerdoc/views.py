# Create your views here.
#searching for words r =c.search('obj*').flags(djapian.resultset.xapian.QueryParser.FLAG_WILDCARD)
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseBadRequest,\
                        HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from jaxerdoc.models import ClassItem, Function, Parameter, Property,\
                            JaxerNameSpace, JavascriptObject, QueuedItem
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from jaxerutils.utils import get_object
import datetime

def document_detail(request, oslug, ctid, objid, template_name = None, message = None):
    '''
        this is a generic type of view function that can display the detail of
        any jaxer documentation class
        
        oslug =          the objects slug
        ctid =           the id of the objects ContentType
        objid =          the id of the object itself
        template_name = (optional) name for the template to send the context to
    
        the template variable containing the object we want to display is 
        set to the lowercase name of the content type with no spaces.
        
        To access a Jaxer Name Space object you would be directed to the template
        
        jaxerdoc/jaxernamespace_detail.html with {{ jaxernamespace }}
        as the root object variable 
        
        Or the Class:
        jaxerdoc/classitem_detail.html with {{ classitem }}
        as the root object variable.
        
        url will be displayed a yourdomain.com/path/to/your-slug/##-####/
    '''
    obj = get_object(ctid, objid)
    template = template_name or "jaxerdoc/%s_detail.html" % obj.get_model_name()
    return render_to_response(template,
                              {"%s" % obj.get_model_name():obj, 'message':message},
                              context_instance = RequestContext(request))


@login_required
def document_activation(request, ctid, objid, key=None):
    ''' 
        allows the user who submitted a new object the 
        chance to make the first major edit
    '''

def diff_test(request, obj_id):
    c = QueuedItem.objects.get(pk = obj_id)
    return render_to_response('jaxerdoc/diff_test.html', {'object':c}, context_instance = RequestContext(request))

def docs_root(request, template_name = "jaxerdoc/documentation_home.html"):
    from jaxerdoc.models import FunctionalityGroup
    groups = FunctionalityGroup.objects.all()
    
    return render_to_response(template_name, {'group_list':groups}, context_instance = RequestContext(request))
