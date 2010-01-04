''' Hotsauce Forms'''
from django import forms
from django.forms.models import ModelForm

class EditableItemForm(ModelForm):
    '''
        this form MUST be subclassed and the model must 
        be set in the meta innerclass
    '''
    from django.contrib.auth.models import User
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
            
        new_item = super(EditableItemForm, self).save()
        if new:
            new_item.editor = editor
            new_item.save()
        # create new ChangeSet
        new_item.send_to_que(old_content, old_name, comment, editor)
