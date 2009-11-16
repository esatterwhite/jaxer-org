from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from photologue.models import Photo
from django.utils.translation import ugettext_lazy as _

# Create your models here.
PRIMARY_LANGUAGE = (
    ('js', 'JavaScript'),
    ('html', 'HTML'),
    ('css','CSS'),
    ('php','PHP'),
    ('ruby','Ruby'),
    ('sql','SQL'),
    ('md','MarkDown'),
    ('shell','Shell')
)
OS_OPTIONS = (
    ('windows','Windows'),
    ('osx','Mac OS-X'),
    ('linux','Linux')              
)
LANGUAGE_PREF = ()

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    #proxie fields to name to reduce join and FK lookups
    f_name =   models.CharField(_('First Name'), max_length=30, 
                                blank=True, editable=False)
    
    l_name =   models.CharField(_('Last Name'), max_length=30, 
                                blank=True, editable=False)
    
    avatar =   models.ForeignKey(Photo)
    about_me = models.TextField(_('About Me'))
    email =    models.CharField(_('Email'), max_length=300, 
                                blank=True, null=True)
    
    os =       models.CharField(_('OS Preference'), 
                                max_length=20, 
                                choices=OS_OPTIONS)
    
    language = models.CharField(_('Language Preference'), 
                                max_length=20, 
                                choices=PRIMARY_LANGUAGE)

    # display preference checks
    display_name = models.BooleanField(_('Display Your Real Name'))
    display_email = models.BooleanField(_('Display Email Address'))
    
    #default manager 
    admin_objects = Manager()
    #common manager
    objects =       Manager()
    def __unicode__(self):
        return "%s" % self.name()
    
    def name(self):
        if self.display_name:
            return "%s %s" %(self.f_name, self.l_name)
        else:
            return self.user.username
    def username(self):
        '''for display use in admin site'''
        return "%s" % self.user.username    
    def is_staff(self):
        '''is the member staff'''
        return bool(self.user.is_staff)  
          
    def save(self, force_insert=False, force_update=False):
        if self.f_name == "" or self.f_name is None:
            self.f_name = self.user.first_name
            self.l_name = self.user.last_name
        
        super(UserProfile, self,).save(force_insert, force_update)