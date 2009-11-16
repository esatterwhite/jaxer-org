''' Hotsauce Forms'''
from django import forms
from django.forms.models import ModelForm
from hotsauce.models import WikiPage
class EditableItemForm(ModelForm):
    from django.contrib.auth.models import User
    author =    forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput())
    comment =   forms.CharField()
    action =    forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = WikiPage

    def save(self):
        ''' DOCSTRING '''
        # get old infor before saving

        comment = self.cleaned_data['comment']
        editor = self.cleaned_data['author']
        if self.instance.id is None:
            old_title = ""
            old_content = ""
            new = True
        else:
            old_title= self.instance.title
            old_content=self.instance.content
            new = False
            
        #Save editable item
        
        new_item = super(EditableItemForm, self).save()
        if new:
            new_item.author = editor
            new_item.save()
        # create new ChangeSet
        new_item.make_new_revision(old_content, old_title, comment, editor)
        