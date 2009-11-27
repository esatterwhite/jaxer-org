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

import xapian
import djapian

djapian.load_indexes()
def ajax_doc_search(request):
    if request.is_ajax():       
        if request.POST:
            try:
                search = request.POST['searchVal']
                if " " in search:
                    search = search.replace(" ", " OR ")
                if "." in search:
                    search = search.replace(".", ' AND ')
                flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
                    |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
                indexers = [ClassItem.indexer, JaxerNameSpace.ns_indexer]
                comp = CompositeIndexer(*indexers)
                res = comp.search(search).flags(flags)
                rlist = [dict(name=x.instance.__unicode__(), 
                              ct_id=x.instance.get_ct_id(),
                              ct=x.instance.get_ct().name,
                              obj_id=x.instance.pk,
                              slug=x.instance.slug,
                              client=bool(x.instance.client_side),
                              server=bool(x.instance.server_side),
                              classname=x.instance.get_ct().name) for x in res]
                return HttpResponse(simplejson.dumps(rlist), 
                                mimetype='text/javascript')
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponse(simplejson.dumps({'error':True}))
    else:
        # can probably change to redirect to a search
        # page view as well
        return HttpResponseBadRequest()
    
def ajax_js_object_search(request):
    import pdb
    pdb.set_trace()
    if request.is_ajax():
        search = request.POST['search']
        flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
            |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
        indexer = JavascriptObject.indexer

        res = indexer.search(search).flags(flags)
        rlist = [dict(name=x.instance.__unicode__(), 
                      ct_id=x.instance.get_ct_id(),
                      ct=x.instance.get_ct().name,
                      obj_id=x.instance.pk) for x in res]
        return HttpResponse(simplejson.dumps(rlist), mimetype='text/javascript')   
    else:
        return HttpResponseBadRequest()
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


def add_parameter_to_object(request, add_to_id, add_to_ct, param_id):
    
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