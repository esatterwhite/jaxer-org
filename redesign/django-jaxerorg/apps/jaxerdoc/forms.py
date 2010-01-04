from django import forms
from django.forms import fields
from jaxerdoc.models import ClassItem, Property, Parameter, Function, JavascriptObject, JaxerNameSpace, QueuedItem, \
    MODERATION_OPTIONS
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from jaxerdoc.widgets import AjaxObjectSearchbar
from jaxerhotsauce.models import ChangeSet
from jaxerutils.utils import get_model_class
from datetime import date
try:
    from jaxerlog.models import UserLogEntry as logger
except ImportError, NameError:
    logger = None
    
class GenericEditForm(forms.ModelForm):
    '''
        this is a generic form that should be used when submitting
        an edit to a wiki-able item. The only visible item will be the content
        area, which will be displayed on the page for people to edit
        
        when saved, a new queueditem will be created
    '''
    editor = forms.ModelChoiceField(User.objects.all(), widget = fields.HiddenInput())
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget = fields.HiddenInput())
    object_id = forms.CharField(widget = fields.HiddenInput())
    at_revision = forms.CharField(widget = fields.HiddenInput())
    content = forms.CharField(widget = forms.Textarea(attrs = {'rows':'30'}))
    comment = forms.CharField(widget = forms.TextInput(attrs = {'class':'width100'}), required = False)
    action = forms.CharField(widget = forms.HiddenInput(), required = False)
    class Meta:
        model = QueuedItem
        exclude = ('moderate', 'submit_date', 'mod_reason', 'add_key', 'key_expired', 'add_summary', 'add_title', 'adding_type')
class GenericAddForm(forms.ModelForm):
    '''
        this form should be used when a user wants to propose the addition 
        of a new item to the docs.
        
        form only displays a field for title and summary. We figure out the rest    
    '''
    types = ContentType.objects.all()
    add_title = forms.CharField(widget = forms.TextInput(attrs = {'class':'width100'}), label = 'Title')
    content_type = forms.ModelChoiceField(types, widget = forms.HiddenInput())
    object_id = forms.CharField(widget = forms.HiddenInput())
    
    add_summary = forms.CharField(widget = forms.Textarea(),
                                   label = 'Summary',
                                   help_text = 'What is it? Why Should we add it?', required = True)
    adding_type = forms.ModelChoiceField(types, widget = forms.HiddenInput())
    action = forms.CharField(widget = forms.HiddenInput())
    editor = forms.ModelChoiceField(User.objects.all(), widget = forms.HiddenInput()) 
    at_revision = forms.CharField(widget = forms.HiddenInput())
    next = forms.CharField(widget = forms.HiddenInput())
    class Meta:
        model = QueuedItem
        exclude = ('content', 'comment', 'moderate', 'mod_reason')
        
    def save(self):
        # if we get an instance, we know the object already exists
        if self.instance.pk is not None:
            raise ValidationError
        else:
            new_item = super(GenericAddForm, self).save()
            
            return new_item
class AddItemModerationForm(forms.ModelForm):
    ''' 
        This form is used by moderators for 
        accepting / rejecting new item proposals
        
        This form holds enough generic data to create any of the
        Document
    '''
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget = fields.HiddenInput())
    object_id = forms.CharField(widget = fields.HiddenInput())
    at_revision = forms.CharField(widget = fields.HiddenInput())
    moderate = forms.CharField(widget = forms.RadioSelect(choices = MODERATION_OPTIONS))
    mod_reason = forms.CharField(label = "Mod Explaination", widget = forms.TextInput(attrs = {'class':'width100'}))
    adding_type = forms.ModelChoiceField(ContentType.objects.all(), widget = fields.HiddenInput())
    add_title = forms.CharField(widget = fields.HiddenInput())
    add_summary = forms.CharField(widget = fields.HiddenInput())
    action = forms.CharField(widget=fields.HiddenInput())
    editor = forms.ModelChoiceField(User.objects.all(), widget = fields.HiddenInput())
    class Meta:
        model = QueuedItem
        # we don't want to moderator to edit the content
        # just moderate it
        exclude = ('submit_date', 'comment', 'add_key', 'key_expired','content')
    
    def save(self):
        mod_decision = self.cleaned_data['moderate']
        if mod_decision == 'approval':
            from hashlib import sha224
            import pdb
            pdb.set_trace()
            
            # get model
            model = self.cleaned_data['adding_type'].model_class()
            
            #populate new item
            new_item = model(name = self.cleaned_data['add_title'],
                             content = self.cleaned_data['add_summary'],
                             editor = self.cleaned_data['editor'],
                             content_type = self.cleaned_data['content_type'],
                             object_id = self.cleaned_data['object_id'],
                             )
            
            #save new item
            new_item.save()
            
            # switch the queue item to the new item, not the item we are
            # adding the new item too
            queue_item = super(AddItemModerationForm, self).save()
            _tmp = queue_item.content_object
            if new_item.get_model_name().lower() == "parameter":
                _tmp.parameters.add(new_item)
            elif new_item.get_model_name().lower() == "property":
                _tmp.properties.add(new_item)
            elif new_item.get_model_name().lower() == "function":
                _tmp.methods.add(new_item)
            _tmp.save()
            _tmp = None

            try:
                from jaxerlog.models import LOG_ADDITION 
                logger.objects.log_action(
                    user_id = new_item.editor.pk,
                    content_type_id = new_item.get_ct_id(),
                    object_id = new_item.pk,
                    action_flag = LOG_ADDITION,
                    change_message = ""
                )
            except ImportError, NameError:
                pass
            
            return new_item, queue_item
        else:
            return None, super(AddItemModerationForm, self).save()
        
class QueueModerationForm(forms.ModelForm):
    '''
        This form is for use by documentation moderators to approve/deny
        current items in the queue

    '''
    
    content_type = forms.ModelChoiceField(ContentType.objects.all(), widget = fields.HiddenInput())
    object_id = forms.CharField(widget = fields.HiddenInput())
    at_revision = forms.CharField(widget = fields.HiddenInput())
    moderate = forms.CharField(widget = forms.RadioSelect(choices = MODERATION_OPTIONS))
    mod_reason = forms.CharField(label = "Mod Explaination", widget = forms.TextInput(attrs = {'class':'width100'}))
    class Meta:
        model = QueuedItem
        # we don't want to moderator to edit the content
        # just moderate it
        exclude = ('add_summary', 'editor', 'content', 'submit_date',
                   'comment', 'add_key', 'key_expired', 'action',
                    'adding_type', 'add_title')
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
            import pdb
            pdb.set_trace()
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
                item = super(QueueModerationForm, self).save()
                if logger is not None:
                    from jaxerlog.models import LOG_ADDITION, LOG_CHANGE
                    if self.instance.action =="new":
                        logger.objects.log_action(
                              user_id = item.editor.pk, 
                              content_type_id = item.content_object.get_ct_id(), 
                              object_id = item.content_object.pk, 
                              action_flag = LOG_ADDITION, 
                              change_message = "added a new document"
                      )
                        
                    else:
                        logger.objects.log_action(
                              user_id = item.content_object.editor.pk, 
                              content_type_id = item.content_object.get_ct_id(), 
                              object_id = item.content_object.pk, 
                              action_flag = LOG_CHANGE, 
                              change_message = 'edited the document'
                      )
                return item
            else:
                # if the decision was a denial
                # just save the changes to the queue object
                
                return super(QueueModerationForm, self).save()
        
