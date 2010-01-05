# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.safestring import EscapeString
from django.template.defaultfilters import force_escape
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from messages.views import compose
from jaxerprofile.forms import MultiUserComposeForm

def escape_code(request, code=""):
    return HttpResponse(EscapeString(request.POST['code']))
def jaxer_home(request):
    return render_to_response('core/homepage.html', 
                             {}, 
                             context_instance=RequestContext(request))
def editor_test(request):
    from jaxerorg.core.forms import EditorForm
    form = EditorForm()
    return render_to_response('core/editortest.html', {'form':form}, context_instance=RequestContext(request))
def search_test(request):    
    if request.POST:
        form = MultiUserComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
        else:
            form = MultiUserComposeForm(request.POST)
    else:
        form = MultiUserComposeForm()
    return render_to_response('searchtest.html', {'form':form}, context_instance=RequestContext(request))

def multi_mail(request):
     return compose(request, form_class=MultiUserComposeForm, template_name='messages/multiusercompose.html') 
def ajax_code_form(request):
    ''' returns HTML code for InsertCodeForm as an unordered list'''
    from jaxerorg.core.forms import InsertCodeForm
    form = InsertCodeForm()
    return HttpResponse(form.as_ul())
def login_user(request, next='/'):
    from jaxerorg.core.forms import LoginForm
    message=None
    if request.is_ajax():
        pass
    else:
        if request.POST:
            login_form = LoginForm(request.POST, initial={'next':next})
            if login_form.is_valid():
                u = login_form.cleaned_data['username']
                p = login_form.cleaned_data['password']
                the_user = authenticate(username = u, password = p)
                if the_user is not None and the_user.is_active:
                    login(request, the_user)
                    if request.GET:
                        redir = request.GET['next'] or '/' 
                    else:
                        redir = login_form.cleaned_data['next'] or next
                    return HttpResponseRedirect(redir)            
                else:
                    message ="username/password did not match"
                    form = LoginForm(request.POST, initial={'next':next})
                    return render_to_response('core/login.html', {'form':form,'message':message}, context_instance=RequestContext(request))
        else:
            form = LoginForm( initial={'next':request.META['HTTP_REFERER']})
            return render_to_response('core/login.html', {'form':form}, context_instance=RequestContext(request))
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
