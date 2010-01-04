from djapian import space, Indexer
from jaxerdoc.models import ClassItem, JavascriptObject, JaxerNameSpace, Property, Parameter, Function
# convert xapian resultset to a list of dictionary
#
# where r is a Xapain ResultSet Object
#
# [x.instance.__dict__ for x in r.all()] - a serializable object
# OR
# [x.__dict__ for x in r.all()]

class JSObjectIndexer(Indexer):
    fields = ['name', 'content', 'search_name']
    tags = [
        ('name','name'),
        ('content','content')
    ]
class ClassItemIndexer(Indexer):
    fields = ['name', 'content', 'search_name']
    tags = [
        ('name','name'),
        ('content','content'),
        ('search_name', 'search_name')
    ]
class JaxerNameSpaceIndexer(Indexer):
    fields = ['name', 'content', 'search_name']
    tags = [
        ('name','name'),
        ('content','content'),
        ('search_name', 'search_name')
    ]
class JaxerFunctionIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]
class JaxerParameterIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]
class JaxerPropertyIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]    
space.add_index(JavascriptObject, JSObjectIndexer, attach_as='indexer')
space.add_index(ClassItem, ClassItemIndexer, attach_as='indexer')
space.add_index(JaxerNameSpace, JaxerNameSpaceIndexer, attach_as='ns_indexer')
space.add_index(Function, JaxerFunctionIndexer, attach_as='indexer')
space.add_index(Parameter, JaxerParameterIndexer, attach_as='indexer')
space.add_index(Property, JaxerPropertyIndexer, attach_as='indexer')