'''        HOTSAUCE VIEWS        '''
#from django.core.urlresolvers import reverse
#from hotsauce.models import ChangeSet, WikiPage
from hotsauce.forms import EditableItemForm
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from hotsauce.models import WikiPage, ChangeSet
# Create your views here.

def wiki_list(request):
    ''' display all wikipages'''
    object_list = WikiPage.objects.all()
    return render_to_response('hotsauce/hotsauce_index.html', 
                              {'object_list':object_list}, 
                              context_instance=RequestContext(request))

@login_required
def add_edit_item(request, item=None, obj_id=None, template_name='hotsauce/hotsuace_wikiitem.html'):
    '''docstrings'''

    try:
        updating = WikiPage.objects.get(pk=obj_id)
    except:
        updating = None
    if request.POST:
        if updating is None:
            form = EditableItemForm(request.POST, request.FILES, initial={'action':'create'})
        else:
            form = EditableItemForm(request.POST, request.FILES, instance=updating,initial={'action':'edit'})
        if form.is_valid():
            form.save()
            return render_to_response('/', {}, context_instance=RequestContext(request))
        else:
            return render_to_response(template_name, {'form':form}, context_instance=RequestContext(request))            
    else:
        form = EditableItemForm(instance=updating, initial={'author':request.user.id, 'action':'edit'})    
    return render_to_response(template_name, {'form':form}, context_instance=RequestContext(request))

def view_changes(request, item=None, obj_id=None, template_name='hotsauce/hotsauce_viewchanges.html'):
    changeset = ChangeSet.objects.get(pk=obj_id)
    html = changeset.display_change_html()
    return render_to_response(template_name, {'html':html}, context_instance=RequestContext(request))