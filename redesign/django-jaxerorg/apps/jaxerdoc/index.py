from djapian import space, Indexer
from jaxerdoc.models import ClassItem, JavascriptObject, JaxerNameSpace
# convert xapian resultset to a list of dictionary
#
# where r is a Xapain ResultSet Object
#
# [x.instance.__dict__ for x in r.all()] - a serializable object
# OR
# [x.__dict__ for x in r.all()]

class JSObjectIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]
class ClassItemIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]
class JaxerNameSpaceIndexer(Indexer):
    fields = ['name', 'content']
    tags = [
        ('name','name'),
        ('content','content')
    ]
space.add_index(JavascriptObject, JSObjectIndexer, attach_as='indexer')
space.add_index(ClassItem, ClassItemIndexer, attach_as='indexer')
space.add_index(JaxerNameSpace, JaxerNameSpaceIndexer, attach_as='ns_indexer')