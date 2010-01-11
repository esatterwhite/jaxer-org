from django.contrib import contenttypes
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from jaxerdoc.forms import GenericAddForm, AddItemModerationForm
from jaxerdoc.models import Parameter, ClassItem, Function, Property
from django.utils import simplejson
def add_object_proposal(request, add_ct_id, ct_id, obj_id):
    '''
        used to create a new object which will be associated to another object
        both types of objects are known, contenttype is retrived from the template
    '''
    #if we got something from the form
    if request.POST:
        form = GenericAddForm(request.POST)
        if form.is_valid():
            # save the form for moderation
            item = form.save()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps({'result':True}))
            else:
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

def add_parameter_to_object(request, add_to_ct_id, add_to_id):
    '''
        This is a wrapper around the generall add object function
        
        Sometimes, we aren't able to get the content type of an object,
        but we know what we are trying to add anyway. So we use this in
        such a case.
    '''
    ct = ContentType.objects.get_for_model(Parameter)
    return(add_object_proposal(request, ct.pk, add_to_ct_id, add_to_id ))
def add_class_to_object(request, add_to_ct_id, add_to_id):
    '''
        This is a wrapper around the generall add object function
        
        Sometimes, we aren't able to get the content type of an object,
        but we know what we are trying to add anyway. So we use this in
        such a case.
    '''
    ct = ContentType.objects.get_for_model(ClassItem)
    return(add_object_proposal(request, ct.pk, add_to_ct_id, add_to_id ))
def add_property_to_object(request, add_to_ct_id, add_to_id):
    '''
        This is a wrapper around the generall add object function
        
        Sometimes, we aren't able to get the content type of an object,
        but we know what we are trying to add anyway. So we use this in
        such a case.
    '''
    ct = ContentType.objects.get_for_model(Property)
    return(add_object_proposal(request, ct.pk, add_to_ct_id, add_to_id ))
