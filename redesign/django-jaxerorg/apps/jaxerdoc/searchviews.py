import pdb
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from djapian.indexer import CompositeIndexer, Indexer
from jaxerdoc.models import ClassItem, JaxerNameSpace, JavascriptObject, \
    Property, Parameter, Function
import pdb

try:
    import xapian
except ImportError:
    xapian = None

    
def ajax_doc_search(request):
    if xapian is None:
        result =[]
        return HttpResponse(simplejson.dumps(result, mimetype="text/javascript"))
    if request.is_ajax():     
        if request.POST:
            try:
                search = request.POST['searchVal']
                if " " in search:
                    search = search.replace(" ", " OR ")
                if "." in search:
                    search = search.replace(".", ' AND ')
                flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
                    |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
                indexers = [ClassItem.indexer, JaxerNameSpace.ns_indexer, Parameter.indexer, Function.indexer]
                comp = CompositeIndexer(*indexers)
                res = comp.search(search).flags(flags)
                rlist = [dict(name=x.instance.__unicode__(), 
                              ct_id=x.instance.get_ct_id(),
                              ct=x.instance.get_ct().name,
                              obj_id=x.instance.pk,
                              slug=x.instance.slug,
                              client=bool(x.instance.client_side),
                              server=bool(x.instance.server_side),
                              classname=x.instance.get_ct().name,
                              url=x.instance.get_absolute_url() or None) for x in res]
                return HttpResponse(simplejson.dumps(rlist), 
                                mimetype='text/javascript')
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponse(simplejson.dumps({'error':True}, mimetype="text/javascript"))
    else:
        # can probably change to redirect to a search
        # page view as well
        return HttpResponseBadRequest()
def ajax_property_search(request):
    if xapian is None:
        result =[]
        return HttpResponse(simplejson.dumps(result, mimetype="text/javascript"))
    if request.is_ajax():       
        if request.POST:
            try:
                search = request.POST['searchVal']
                if " " in search:
                    search = search.replace(" ", " OR ")
                if "." in search:
                    search = search.replace(".", ' AND ')
                flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
                    |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
                indexer = Property
                res = indexer.search(search).flags(flags)
                rlist = [dict(name=x.instance.__unicode__(), 
                              ct_id=x.instance.get_ct_id(),
                              ct=x.instance.get_ct().name,
                              obj_id=x.instance.pk,
                              slug=x.instance.slug,
                              client=bool(x.instance.client_side),
                              server=bool(x.instance.server_side),
                              itemname=x.instance.get_ct().name,
                              url=x.instance.get_absolute_url() or None) for x in res]
                return HttpResponse(simplejson.dumps(rlist), 
                                mimetype='text/javascript')
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponse(simplejson.dumps({'error':True}, mimetype="text/javascript"))
    else:
        # can probably change to redirect to a search
        # page view as well
        return HttpResponseBadRequest()
def ajax_function_search():
    pdb.set_trace()
    if request.is_ajax():
        pass
    else:
        return HttpResponseBadRequest()

def ajax_js_object_search(request):
    pdb.set_trace()
    if request.is_ajax():
        search = request.POST['search']
        flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
            |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
        indexer = JavascriptObject.indexer

        res = indexer.search(search).flags(flags)
        rlist = [dict(name=x.instance.__unicode__(), 
                      ct_id=x.instance.get_ct_id(),
                      ct=x.instance.get_ct().name,
                      obj_id=x.instance.pk) for x in res]
        return HttpResponse(simplejson.dumps(rlist), mimetype='text/javascript')   
    else:
        return HttpResponseBadRequest()