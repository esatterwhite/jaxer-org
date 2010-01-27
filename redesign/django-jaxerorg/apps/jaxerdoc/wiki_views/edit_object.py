from django.contrib import contenttypes
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from jaxerdoc.forms import GenericAddForm, AddItemModerationForm
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from jaxerutils.utils import get_object
@login_required
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