from django import forms
from django.forms import fields
from jaxerdoc.models import ClassItem,Property, Parameter, Function, JavascriptObject, JaxerNameSpace, QueuedItem
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
        an edit to a wiki item. The only visible item will be the content
        area, which will be displayed on the page for people to edit
        
        when saved, a new queueditem will be created
    '''
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget=fields.HiddenInput())
    object_id =    forms.CharField(widget=fields.HiddenInput())
    at_revision =  forms.ModelChoiceField(ChangeSet.objects.all(), widget=fields.HiddenInput())
    content =      forms.CharField(widget=forms.Textarea(attrs={'rows':'30'}))
    class Meta:
        model = QueuedItem
        exclude = ['approve', 'deny']
class QueDocumentationForm(forms.ModelForm):
    '''
        this form MUST be subclassed and the model must 
        be set in the meta innerclass
    '''
    editor =    forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput())
    comment =   forms.CharField()
    action =    forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = ''

    def save(self):
        ''' DOCSTRING '''
        # get old infor before saving

        comment = self.cleaned_data['comment']
        editor = self.cleaned_data['editor']
        if self.instance.id is None:
            old_name = ""
            old_content = ""
            new = True
        else:
            old_name= self.instance.name
            old_content=self.instance.content
            new = False
            
        new_item = super(QueDocumentationForm, self).save()
        if new:
            new_item.editor = editor
            new_item.save()
        # create new ChangeSet
        new_item.send_to_que(old_content, old_name, comment, editor)
        