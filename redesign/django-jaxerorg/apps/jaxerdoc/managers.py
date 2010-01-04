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
class OnlineObjectManager(Manager):
    '''for the JavascriptObject Class'''
    def get_query_set(self):
        default_query_set = super(CustomObjectManager, self).get_query_set()    
        return default_query_set.filter(on_line = True)
        
class GlobalFunctionManager(Manager):
    def get_query_set(self):
        default_query_set = super(GlobalFunctionManager, self).get_query_set()    
        return default_query_set.filter(is_global=True)

class UnmanagedQueItemManager(Manager):
    '''returns all of the Queued Items that have not been moderated'''
    def get_query_set(self):
        default_query_set = super(UnmanagedQueItemManager, self).get_query_set()
        return default_query_set.filter(moderate=None)
    
class ApprovedQueItemManager(Manager):
    '''returns all of the Queued Items that have not been moderated'''
    def get_query_set(self):
        default_query_set = super(ApprovedQueItemManager, self).get_query_set()
        return default_query_set.filter(moderate='approval')
    
class DeniedQueItemManager(Manager):
    '''returns all of the Queued Items that have not been moderated'''
    def get_query_set(self):
        default_query_set = super(DeniedQueItemManager, self).get_query_set()
        return default_query_set.filter(moderate='denial')     