from django.db.models import Manager

class NaitiveObjectManager(Manager):
    def get_query_set(self):
        default_query_set= super(NaitiveObjectManager,self).get_query_set()

        return default_query_set.filter(naitive = True)
    
class CustomObjectManager(Manager):
    '''for the JavascriptObject Class'''
    def get_query_set(self):
        default_query_set = super(CustomObjectManager, self).get_query_set()
        
        return default_query_set.filter(naitive = False)
class GlobalFunctionManager(Manager):
    def get_query_set(self):
        default_query_set = super(GlobalFunctionManager, self).get_query_set()
        
        return default_query_set.filter(is_global=True)