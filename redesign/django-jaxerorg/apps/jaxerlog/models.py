from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from jaxerlog.managers import MemberLogManager

LOG_ADDITION = 1
LOG_CHANGE = 2
LOG_DELETION = 3

class MemberLogEntry(models.Model):
    '''gives the ability to effectivly track any objects on your site'''
    action_time = models.DateTimeField('Action Time', auto_now=True)
    member = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.IntegerField('Object Id', blank=True, null=True)
    action_flag = models.PositiveSmallIntegerField('Action Flag')
    change_message = models.TextField('Action Message', blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = MemberLogManager()
    
    def __repr__(self):
        '''representation'''
        return smart_unicode(self.action_time)
    def is_addition(self):
        '''boolean check'''
        return self.action_flag == LOG_ADDITION
    def __unicode__(self):
        '''unicode representation'''
        return "%s just %s a %s" %(self.member.name, self.change_message, self.content_type)
    def is_change(self):
        '''boolean check'''
        return self.action_flag == LOG_CHANGE
    def __str__(self):
        '''text representation'''
        return self.__unicode__() 
    def is_deletion(self):
        '''boolean check'''
        return self.action_flag == LOG_DELETION
    def get_edited_object(self):
        '''returns content object'''
        return self.content_type.get_object_for_this_type(pk=self.object_id)  
    def get_absolute_url(self):
        '''returns url of the content object'''
        return self.content_object.get_absolute_url()

    class Meta:
        db_table = 'jaxer_site_log' 
        ordering = ['-action_time']
