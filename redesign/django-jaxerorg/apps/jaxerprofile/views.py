# Create your views here.
from jaxerprofile.models import  UserProfile
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import simplejson
def ajax_member_search(request):
    '''finds site members ( profile objects ) based on username'''

    if request.is_ajax():
        profiles = UserProfile.objects.filter(user__username__istartswith=request.POST['q'])
        ulist = [dict(user=x.user.username, 
                      ct_id=x.get_ct_id(), 
                      obj_id=x.pk )for x in profiles]
        return HttpResponse(simplejson.dumps(ulist), mimetype="application/javascript")