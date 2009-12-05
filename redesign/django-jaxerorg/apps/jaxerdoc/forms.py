from django import forms
from django.forms import fields
from jaxerdoc.models import ClassItem,Property, Parameter, Function, JavascriptObject, JaxerNameSpace, QueuedItem,\
    MODERATION_OPTIONS
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from jaxerdoc.widgets import AjaxObjectSearchbar
from jaxerhotsauce.models import ChangeSet
class AddParameterForm(forms.ModelForm):
    param_type =   forms.CharField(widget=AjaxObjectSearchbar())
    editor =       forms.ModelChoiceField(User.objects.all(), widget=fields.HiddenInput())
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    
    class Meta:
        model = Parameter

class GenericEditForm(forms.ModelForm):
    from jaxerdoc.models import MODERATION_OPTIONS
    '''
        this is a generic form that should be used when submitting
        an edit to a wiki-able item. The only visible item will be the content
        area, which will be displayed on the page for people to edit
        
        when saved, a new queueditem will be created
    '''
    editor =       forms.ModelChoiceField(User.objects.all(), widget=fields.HiddenInput())
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    at_revision =  forms.CharField(widget=fields.HiddenInput())
    content =      forms.CharField(widget=forms.Textarea(attrs={'rows':'30'}))
   
    class Meta:
        model = QueuedItem
        exclude = ('moderate','submit_date')
class QueueModerationForm(forms.ModelForm):
    '''
        This form is for use by documentation moderators to approve/deny
        current items in the queue
    '''
    
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    at_revision =  forms.CharField(widget=fields.HiddenInput())
    content =      forms.CharField(widget=forms.Textarea(attrs={'rows':'30'}))
    moderate =     forms.CharField(widget=forms.RadioSelect(choices=MODERATION_OPTIONS, attrs={'class':'fl'}))
    
    class Meta:
        model = QueuedItem
        
    def save(self):
        '''
            Queued items are only intended to be moderated once, so we
            want to check to see if the moderate field is not NULL.
            If it is not NULL, we know it has been moderated already
        '''
        # their should never be an 'new' instance of a queueditem
        # but better safe than sorry
        if self.instance.id is None:
            return False
        else:
            moderated = self.instance.modaerate
            
        
        if moderated is None:
            # if moderated is None
            # we want to apply the edit to the item
            # and create a changeset for the item.
            
            # update the instance
            super(QueueModerationForm, self).save()
            pass
        else:
            pass
            # if moderated is not None
            # it has already been moderated and we 
            # do not want to do anything!
            super(QueueModerationForm,self).save()
        