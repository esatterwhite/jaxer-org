from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from jaxerdoc.models import ClassItem, Function, Parameter, Property, JaxerNameSpace, QueuedItem
from django.template.context import RequestContext

def queue_manager(request):
    queue = QueuedItem.unmanaged.all()
    return render_to_response('jaxerdoc/queue_manager.html', 
                              {'queue':queue,'MODERATE':True}, 
                              context_instance=RequestContext(request))
    
def queue_detail(request, queue_id):
    
    return    
def show_difference(request, que_id):
    ''' returns the HTML fragment to be injected into page '''
    pass
def show_compare(request, que_id):
    
    que = QueuedItem.objects.get(pk=que_id)
    
    return render_to_response('jaxerdoc/compare_with_que.html', 
                             {'queueditem':que}, 
                              context_instance=RequestContext(request))