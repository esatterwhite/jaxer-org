from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from jaxerdoc.models import ClassItem, Function, Parameter, Property, JaxerNameSpace, QueuedItem
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('jaxerdoc.can_moderate')
def queue_manager(request, filter=None):
    if filter is None:
        queue = QueuedItem.unmanaged.all()

    elif filter == 'all':
        queue = QueuedItem.objects.all()
    else:
        queue = QueuedItem.objects.filter(moderate=filter)
    if queue.filter(moderate=None).count() == 0:
        mod = False
    else:
        mod = True  
    return render_to_response('jaxerdoc/queue_manager.html',
                              {'queue':queue, 'MODERATE':mod},
                              context_instance=RequestContext(request))
    
def show_difference(request, queue_id):
    queueitem = QueuedItem.objects.get(pk=queue_id)
    html = queueitem.display_diff_html()
    if request.is_ajax():
        return HttpResponse(html, mimetype="text/html")
    else:
        return render_to_response('jaxerdoc/queue_difference.html',
                                  {'difference':html},
                                  context_instance=RequestContext(request))

@login_required
@permission_required('jaxerdoc.can_moderate')
def moderate_queue(request, queue_id):
    from jaxerdoc.forms import QueueModerationForm
    from django.core.urlresolvers import reverse
    queue = QueuedItem.objects.get(pk=queue_id)
    if request.POST:
        if queue.is_moderated():
            
            return HttpResponseRedirect(reverse('jaxerdoc_queue_moderation'))
        form = QueueModerationForm(request.POST, instance=queue)
        if form.is_valid():
            form.save()
            m = "you have successfully moderated: %s." % queue
            request.user.message_set.create(message=m) 
            return HttpResponseRedirect(reverse('jaxerdoc_queue_moderation'))
        else:
            form = QueueModerationForm(request.POST, instance=queue)   
    else:
        form = QueueModerationForm(instance=queue)
    return render_to_response('jaxerdoc/moderate_queueitem.html',
                                  {'form':form, 'queueitem':queue},
                                  context_instance=RequestContext(request))
