from django.contrib import contenttypes
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from jaxerdoc.forms import GenericAddForm, AddItemModerationForm

def add_object_proposal(request, add_ct_id, ct_id, obj_id):
    #if we got something from the form
    if request.POST:
        form = GenericAddForm(request.POST)
        if form.is_valid():
            # save the form for moderation
            item = form.save()
            return HttpResponseRedirect(form.cleaned_data['next'] or '/') 
    else:
        form = GenericAddForm(initial={'action':'new', 
                                       'adding_type':add_ct_id,
                                       'editor':request.user.pk,
                                       'at_revision':1,
                                       'content_type':ct_id,
                                       'object_id':obj_id,
                                       'next':request.META['HTTP_REFERER']})
        
        if request.is_ajax():
            #via Request.HTML
            return HttpResponse(form.as_ul())
        else:
            return render_to_response('small_form_box.html', {'form':form}, context_instance=RequestContext(request))
