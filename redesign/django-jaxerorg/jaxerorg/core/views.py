# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.safestring import EscapeString
from django.http import HttpResponse

def escape_code(request, code=""):
    return HttpResponse(EscapeString(request.POST['code']))

def jaxer_home(request):
    return render_to_response('core/homepage.html', 
                             {}, 
                             context_instance=RequestContext(request))

def editor_test(request):
    return render_to_response('core/editortest.html', {}, context_instance=RequestContext(request))
    
def ajax_code_form(request):
    ''' returns HTML code for InsertCodeForm as an unordered list'''
    from jaxerorg.core.forms import InsertCodeForm
    form = InsertCodeForm()
    return HttpResponse(form.as_ul())
