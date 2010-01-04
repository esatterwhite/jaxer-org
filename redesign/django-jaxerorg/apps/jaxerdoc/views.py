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

def ajax_document_edit(request, ctid, objid, template_name = None):  
    from jaxerdoc.forms import GenericEditForm
    from jaxerdoc.utils import get_object
    doc = get_object(ctid, objid)
    if request.is_ajax():   
        if request.POST:
            form = GenericEditForm(request.POST, instance = doc)
            if form.is_valid():
                return HttpResponse(simplejson.dumps({'message':"Success!"}),
                                    mimetype = "application/javascript")
        else:
            obj = get_object(ctid, objid)
            form = GenericEditForm(initial = {'editor':request.user.id,
                                            'object_id':objid,
                                            'content_type':ctid,
                                            'content':obj.get_html_content(),
                                            'at_revision':obj.version_number(),
                                            'action':'edit'})
            # the client is expecting an HTML fragment
            return HttpResponse(form.as_ul())
    #we are submitting the form via the html <input> element for simplicity's sake
    else:  
        if request.POST:
            # we don't pass an instance, becase we are creating a QueuedItem, not a new document item(yet)
            form = GenericEditForm(request.POST)
            message = {}
            if form.is_valid():
                form.save()
            else:
                message['class'] = 'error'
                message['message'] = form.errors.keys()[0]
            type = ContentType.objects.get(pk = ctid)
            model = type.model_class()
            obj = model.objects.get(pk = objid)                
            template = "jaxerdoc/%s_detail.html" % type.model
            context = {"%s" % type.model:obj, 'message':message}
            return direct_to_template(request, template, extra_context = context)
    return HttpResponseRedirect(doc.get_absolute_url())
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
