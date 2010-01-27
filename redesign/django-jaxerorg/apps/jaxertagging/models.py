
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from jaxerutils.models import SelfAwareModel
from django.db.models import Manager

# Create your models here.
class RelatedObject(SelfAwareModel):
    ''' 
        much like the idea of tagging, RelatedObjects are generic
        way to relate any two objects together without knowing what
        they are before hand. This allows users to "Tag" objects with
        other objects rather than just strings; automatically creating 
        links between objects with out having to know much about the objects.
    '''
    # this content item is associated with this object
    _proxy_name  =    models.CharField(max_length=300, blank=True, null=True, editable=False)
    content_type =    models.ForeignKey(ContentType, verbose_name=_("Parent Object Type"))
    object_id =       models.PositiveIntegerField(_("Parent Object ID"))
    content_object =  generic.GenericForeignKey('content_type', 'object_id')
    
    # this content itme is this object
    related_type =    models.ForeignKey(ContentType, verbose_name=_("Related Object Type"),
                                        related_name="relatedtype", 
                                        blank=True, null=True)
    related_obj_id =  models.PositiveIntegerField(_("Related Object ID"), blank=True)
    related_object =  generic.GenericForeignKey('related_type', 'related_obj_id')
    
    objects  =   Manager()
    
    def __unicode__(self):
        return self._proxy_name
    def get_absolute_url(self):
        return self.related_object.get_absolute_url()
    def save(self, force_insert=False, force_update=False):
        if self._proxy_name is None:
            self._proxy_name = self.related_object.__unicode__()
        super(RelatedObject, self).save(force_insert, force_update)