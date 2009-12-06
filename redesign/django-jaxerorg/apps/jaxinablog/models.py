from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from tagging.fields import TagField
from django_extensions.db.models import TimeStampedModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
STATUS_OPTIONS = (
      (1,'Draft'),
      (2,'Published')
)

class RelatedContent(models.Model):
    # this content item is associated with this object
    content_type =    models.ForeignKey(ContentType)
    object_id =       models.PositiveIntegerField()
    content_object =  generic.GenericForeignKey('content_type', 'object_id')
    
    # this content itme is this object
    related_type =    models.ForeignKey(ContentType, related_name="relatedtype", blank=True, null=True)
    related_obj_id = models.PositiveIntegerField(blank=True)
    related_object =  generic.GenericForeignKey('related_type', 'related_type_id')
    
class StandardBlogEntry(TimeStampedModel):
    title =           models.CharField(_('Title'),max_length=255, blank=False)
    status =          models.PositiveSmallIntegerField(_('Status'), choices=STATUS_OPTIONS)
    content =         models.TextField(_('Body'))
    initial_publish = models.BooleanField(editable=False)

    related_content = generic.GenericRelation(RelatedContent)
    def __unicode__(self):
        return self.title
    class Meta:
        ordering =            ('-created',)
        verbose_name =        'Blog Entry'
        verbose_name_plural = 'Blog Entries'
        
class SiteBlog(models.Model):
    '''
        A Multi user blog. Only Specifiec userers will be allowed
        to makes posts
    '''
    title =           models.CharField(max_length=255, blank=False)
    entries =         models.ManyToManyField(StandardBlogEntry, blank=True, null=True)
    allowed_users =   models.ManyToManyField(User, blank=False)
    
class UserBlog(models.Model):
    owner =           models.ForeignKey(User)
    '''a blog intended for use by a single user'''
    title =           models.CharField(max_length=255, blank=False)
    entries =         models.ManyToManyField(StandardBlogEntry)
    
    def __unicode__(self):
        return self.title
    