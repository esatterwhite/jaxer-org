from django_extensions.db.models import TimeStampedModel
from django.contrib.contenttypes.models import ContentType
# generic - can go on anything
class SelfAwareModel(TimeStampedModel):
    '''
        An Abstract model: models which subclass the SelfAwareModel
        will have a series of methods that give quick access to that
        model's meta information:
        
        Content Type & it's ID
        App Label
        Model Name
        Class Name
        
        The aim is to make working with generic models easier from a
        template as generic relations offer a good deal of information
        about the related object, but accessing information about the 
        target object/model itself can be frustrating.
        
        Way to add Standarized functionality with out changing model strucure
    '''
    def get_ct(self):
        return ContentType.objects.get_for_model(self)
    
    def get_ct_id(self):
        return self.get_ct().id
    
    def get_app_label(self):
        return self.get_ct().app_label
    
    def get_model_name(self):
        return self.get_ct().model
    
    def get_class_name(self):
        return self._meta.verbose_name
        
    class Meta:
        abstract = True    