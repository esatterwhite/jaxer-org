# Create your views here.
#searching for words r =c.search('obj*').flags(djapian.resultset.xapian.QueryParser.FLAG_WILDCARD)
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from djapian.indexer import Indexer, CompositeIndexer
from jaxerdoc.models import ClassItem, Function, Parameter, Property, JaxerNameSpace, JavascriptObject
from django.template.context import RequestContext

def document_detail(request, oslug, ctid, objid, template_name=None):
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
    
    type = ContentType.objects.get(pk=ctid)
    model = type.model_class()
    obj = model.objects.get(pk=objid)
    
    template = template_name or "jaxerdoc/%s_detail.html" % type.model
    return render_to_response(template, {"%s" % type.model:obj}, context_instance=RequestContext(request))


def add_parameter_to_object(request, add_to_id, add_to_ct):
    
    ''' ajax view function returning html text '''
    from jaxerdoc.forms import AddParameterForm
    from django.db.models import Q
    from django.template.loader import render_to_string
    if request.is_ajax():
        if request.POST:
            try:
                obj_ct = ContentType.objects.get(pk=add_to_ct)
            except:
                obj_ct=None
            new_param = AddParameterForm(request.POST, request.FILES)
            #link the objects
            new_param.content_type = obj_ct
            new_param.object_id = add_to_id
            
            new_param.save()
            
            #return true to ajax call
        else:
            form = AddParameterForm(initial={'editor':request.user.id})
            html = render_to_string('jaxerdoc/formrender.html', {'form':form})
            return HttpResponse(html)
    else:
        pass
def add_property_to_object(request):
    pass
def add_function_to_object(request):
    pass