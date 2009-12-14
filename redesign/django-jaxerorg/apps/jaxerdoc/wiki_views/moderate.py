from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from jaxerdoc.models import QueuedItem
from django.template.context import RequestContext
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('jaxerdoc.can_moderate_docs')
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
    
def show_difference(request, queue_id, version=None):
    
    queueitem = QueuedItem.objects.get(pk=queue_id)
    html = queueitem.display_diff_html()
    if request.is_ajax():
        return HttpResponse(html, mimetype="text/html")
    else:
        return render_to_response('jaxerdoc/queue_difference.html',
                                  {'difference':html},
                                  context_instance=RequestContext(request))

@login_required
@permission_required('jaxerdoc.can_moderate_docs')
def moderate_queue(request, queue_id):
    '''send the moderator to a page which displays the current document sta
        and the proposed change for approval or denial
    '''
    from jaxerdoc.forms import QueueModerationForm
    from django.core.urlresolvers import reverse
    queue = QueuedItem.objects.get(pk=queue_id)

    if request.POST:
        if queue.is_moderated():
            return HttpResponseRedirect(reverse('jaxerdoc_queue_moderation'))
        form = QueueModerationForm(request.POST, instance=queue)
        if form.is_valid():

            form.save()
            m = 'you have successfully moderated: %s.' % queue
            # send a message to the person who submitted the edit
            from messages.models import Message
            from django.template.loader import render_to_string
            
            if form.cleaned_data['moderate'] == 'approval': moderation = 'approved'
            else: moderation = 'rejected'
            message = render_to_string('jaxerdoc/wiki_%s_message.txt' % moderation, 
                                       {
                                            'moderation':moderation,
                                            'message':form.cleaned_data['mod_reason'],
                                            'from':request.user
                                        })
            if queue.action == 'new':
                sub ='Wiki Submission: %s %s' % (queue.add_title, moderation)
            else:
                sub ='Wiki Submission: %s %s' % (queue.content_object.name, moderation)
            pm = Message(subject = sub,
                         sender=request.user,
                         body=message,
                         recipient=queue.editor) 
            pm.save()             
            request.user.message_set.create(message=m) 
            return HttpResponseRedirect(reverse('jaxerdoc_queue_moderation'))
        else:
            form = QueueModerationForm(request.POST, instance=queue)   
    else:
        form = QueueModerationForm(instance=queue)
    return render_to_response('jaxerdoc/moderate_queueitem_%s.html' % queue.action,
                                  {'form':form, 'queueitem':queue},
                                  context_instance=RequestContext(request))
    
@login_required
@permission_required('jaxerdoc.can_moderate_docs')
def moderate_new_object(request, queue_id):
    import pdb
    pdb.set_trace()
    '''this function handels the moderations of new item proposals'''
    from jaxerdoc.forms import GenericAddForm, AddItemModerationForm
    # when the moderator submits decision
    queue = QueuedItem.objects.get(pk=queue_id)
    if queue.add_key is not None or queue.key_expired:
        # we know the item has been moderated
        pass
    
    if request.POST:
        form = AddItemModerationForm(request.POST)
        if form.is_valid():
            m=''
            item = form.save()
            request.user.message_set.create(message=m)
    # when the moderator wants to review item
    else:
        form = AddItemModerationForm(instance=queue)
    return render_to_response('jaxerdoc/moderate_queueitem_%s.html' % queue.action,
                                  {'form':form, 'queueitem':queue},
                                  context_instance=RequestContext(request))

