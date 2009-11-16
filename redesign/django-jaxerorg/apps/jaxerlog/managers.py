from django.utils.encoding import smart_unicode
from django.db import models
class MemberLogManager(models.Manager):
    '''log manager functions'''
    def log_action(self, user_id, content_type_id, object_id, 
                   action_flag, change_message=''):
        '''logs an action'''
        log = self.model(None, None, user_id, content_type_id, 
                       smart_unicode(object_id), action_flag, change_message)
        log.save()
        
