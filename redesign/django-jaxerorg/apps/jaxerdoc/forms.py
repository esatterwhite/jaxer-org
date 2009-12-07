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
    comment =      forms.CharField(widget=forms.TextInput(attrs={'class':'width100'}), required=False)
    class Meta:
        model = QueuedItem
        exclude = ('moderate','submit_date','mod_reason')
class QueueModerationForm(forms.ModelForm):
    '''
        This form is for use by documentation moderators to approve/deny
        current items in the queue
    '''
    
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    at_revision =  forms.CharField(widget=fields.HiddenInput())
    moderate =     forms.CharField(widget=forms.RadioSelect(choices=MODERATION_OPTIONS))
    mod_reason =   forms.CharField(label="Mod Explaination",widget=forms.TextInput(attrs={'class':'width100'}))
    class Meta:
        model = QueuedItem
        # we don't want to moderator to edit the content
        # just moderate it
        exclude = ('editor', 'content', 'submit_date', 'comment')
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
            # we have an unmoderated queue objec
            mod_decision = self.cleaned_data['moderate']
            if mod_decision == 'approval':
                from diff_match_patch.diff_match_patch import diff_match_patch
                _dmp = diff_match_patch()
                current_doc = self.instance.content_object
                old_html = current_doc.get_html_content()
                current_doc.content = self.instance.content
                
                # save the HTML to the document
                current_doc.save()
                #make revision
                current_doc.make_new_revision(old_html, 
                                              current_doc.name, 
                                              self.instance.comment, 
                                              self.instance.editor)
                # save plain text for search
                current_doc.make_indexable()
                # save the queue item
                super(QueueModerationForm, self).save()
                
                
            else:
                # if the decision was a denial
                # just save the changes to the queue object
                
                super(QueueModerationForm, self).save()
        