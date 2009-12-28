# Create your views here.
#searching for words r =c.search('obj*').flags(djapian.resultset.xapian.QueryParser.FLAG_WILDCARD)
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from jaxerdoc.models import ClassItem, Function, Parameter, Property, JaxerNameSpace, JavascriptObject, \
    QueuedItem
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
                return HttpResponse(
                                    simplejson.dumps({'message':"Success!"}),
                                    mimetype = "application/javascript"
                                    )
        else:
            obj = get_object(ctid, objid)
            form = GenericEditForm(initial = {'editor':request.user.id,
                                            'object_id':objid,
                                            'content_type':ctid,
                                            'content':obj.get_html_content(),
                                            'at_revision':obj.version_number(),
                                            'action':'edit'
                                            })
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

def add_parameter_to_object(request, add_to_id, add_to_ct):
    
    ''' ajax view function returning html text '''
    from jaxerdoc.forms import AddParameterForm
    from django.db.models import Q
    from django.template.loader import render_to_string
    if request.is_ajax():
        if request.POST:
            try:
                obj_ct = ContentType.objects.get(pk = add_to_ct)
            except:
                obj_ct = None
            new_param = AddParameterForm(request.POST, request.FILES)
            #link the objects
            new_param.content_type = obj_ct
            new_param.object_id = add_to_id
            
            new_param.save()
            
            #return true to ajax call
        else:
            form = AddParameterForm(initial = {'editor':request.user.id})
            html = render_to_string('jaxerdoc/formrender.html', {'form':form})
            return HttpResponse(html)
    else:
        pass
def diff_test(request, obj_id):
    c = QueuedItem.objects.get(pk = obj_id)
    return render_to_response('jaxerdoc/diff_test.html', {'object':c}, context_instance = RequestContext(request))

def docs_root(request, template_name = "jaxerdoc/documentation_home.html"):
    from jaxerdoc.models import FunctionalityGroup
    groups = FunctionalityGroup.objects.all()
    
    return render_to_response(template_name, {'group_list':groups}, context_instance = RequestContext(request))
