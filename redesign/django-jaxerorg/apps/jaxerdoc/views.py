# Create your views here.
#searching for words r =c.search('obj*').flags(djapian.resultset.xapian.QueryParser.FLAG_WILDCARD)
from django.utils import simplejson
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from djapian.indexer import Indexer, CompositeIndexer
from jaxerdoc.models import ClassItem, Function, Parameter, Property, JaxerNameSpace, JavascriptObject
from django.template.context import RequestContext
import xapian
import djapian

djapian.load_indexes()


def ajax_doc_search(request):
    import pdb
    pdb.set_trace()
    if request.POST:
        try:
            search = request.POST['q']
            if " " in search:
                search = search.replace(" ", " OR ")
            flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
                |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
            indexers = [ClassItem.indexer, JaxerNameSpace.ns_indexer]
            comp = CompositeIndexer(*indexers)
            res = comp.search(search).flags(flags)
            rlist = [dict(name=x.instance.__unicode__(), 
                          ct=x.instance.get_ct_id(),
                          client=bool(x.instance.client_side),
                          server=bool(x.instance.server_side),
                          classname=x.instance.get_class_name()) for x in res]
            return HttpResponse(simplejson.dumps(rlist), 
                            mimetype='text/javascript')
        except:
            return HttpResponseBadRequest()

def document_detail(request, oslug, ctid, objid, template_name=None):
    type = ContentType.objects.get(pk=ctid)
    model = type.model_class()
    obj = model.objects.get(pk=objid)
    
    template = template_name or "jaxerdoc/%s_detail.html" % type.model
    return render_to_response(template, {'object':obj}, context_instance=RequestContext(request))