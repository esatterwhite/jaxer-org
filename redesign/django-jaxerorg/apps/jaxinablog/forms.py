from django import forms
from jaxinablog.models import UserBlog, StandardBlogEntry, STATUS_OPTIONS
from jaxerorg.core.widgets import MooEditor
from django.contrib.contenttypes.models import ContentType
try:
    from jaxerlog.models import UserLogEntry as logger
except ImportError:
    logger = None

class BlogPostForm(forms.ModelForm):
    status =  forms.CharField(widget=forms.RadioSelect(choices=STATUS_OPTIONS))
    content = forms.CharField(wiget=MooEditor(attrs={'rows':'20'}))
    
    class Meta:
        model = StandardBlogEntry
        exclude =('entries', )
        
    def save(self):
        import pdb
        pdb.set_trace()
        new = None
        if self.instance.id is None:
            # we know to log an addition
            new = True
        else:
            # we know to log a change
            new = False
            
        if not self.instance.is_published and self.cleaned_data['status']==2:
            # if the current object hasn't been published
            # and if the incomming object is set to be published
            # we can log an addition
            if logger is not None:
                
                from jaxerlog.models import LOG_ADDITION
                logger.objects.log_action(
                    user_id         = self.instance.editor.id, 
                    content_type_id = ContentType.objects.get_for_model(self.instance).pk,
                    object_id       = self.instance.id,
                    action_flag     = LOG_ADDITION,
                    change_message = 'added a new'
                )
        
        #super(BlogPostForm, self).save()
class UserBlogForm(forms.ModelForm):
    
    class Meta:
        model = UserBlog
        
