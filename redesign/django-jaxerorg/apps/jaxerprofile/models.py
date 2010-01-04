from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from photologue.models import Photo
from django.utils.translation import ugettext_lazy as _
from jaxerutils.models import SelfAwareModel
# Being a javascript site, the language list should
# stay focused on web orientated languages
PRIMARY_LANGUAGE = (
    ('js', 'JavaScript'),
    ('html', 'HTML'),
    ('css','CSS'),
    ('php','PHP'),
    ('python','Python'),
    ('perl', 'Perl'),
    ('ruby','Ruby'),
    ('sql','SQL'),
    ('java', 'Java'),
    ('asp', 'ASP/ASP.Net'),
    ('cpp', 'C/C++'),
    ('as3','ActionScript'),
    
)
OS_OPTIONS = (
    ('windows','Windows'),
    ('osx','Mac OS-X'),
    ('linux','Linux'),
    ('unix', 'UNIX')              
)
STAFF_RANK = (
    ('ceo', 'CEO/President'),
    ('chair', 'Chairman'),
    ('advisor', 'Advisor'),
    ('support', 'Support Staff'),
    ('web', 'Website Staff')          
)

class UserProfile(SelfAwareModel):
    user = models.ForeignKey(User)
    #proxie fields to name to reduce join and FK lookups
    f_name =        models.CharField(_('First Name'), max_length=30, 
                                        blank=True, editable=False)
    
    l_name =        models.CharField(_('Last Name'), max_length=30, 
                                        blank=True, editable=False)
    
    avatar =        models.ForeignKey(Photo)
    about_me =      models.TextField(_('About Me'))
    email =         models.CharField(_('Email'), max_length=300, 
                                         blank=True, null=True)
    rank =          models.CharField(_('Rank'), max_length=20,
                                        choices=STAFF_RANK)
    
    os =            models.CharField(_('OS Preference'), 
                                        max_length=20, 
                                        choices=OS_OPTIONS)
    
    language =      models.CharField(_('Language Preference'), 
                                        max_length=20, 
                                        choices=PRIMARY_LANGUAGE)
    website =       models.CharField(_('Website'), max_length=300)
    
    # display preference checks
    display_name =  models.BooleanField(_('Display Your Real Name'))
    display_email = models.BooleanField(_('Display Email Address'))
    
    #proxie to forum posts
    post_count  =   models.PositiveIntegerField(default=0, editable=False)
    wiki_points =   models.PositiveIntegerField(default=0)
    
    #default manager 
    admin_objects = Manager()
    #common manager
    objects =       Manager()
    
    def __unicode__(self):
        return "%s" % self.name()
    def get_absolute_url(self):
        return u'/core/'
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
    def increment_post_count(self):
        self.post_count += 1
        self.save()
    def decrement_post_count(self):
        self.post_count -= 1
        self.save()
    def increment_wiki_point(self):
        self.wiki_points += 1
        self.save()
    def decrement_wiki_points(self):
        self.wiki_points -= 1
        self.save()
    def assign_wiki_points(self, points=0):
        self.wiki_points += points
        self.save()          
    def save(self, force_insert=False, force_update=False):
        '''attempts to fill in name proxie fields on save'''
        if self.f_name == "" or self.f_name is None:
            self.f_name = self.user.first_name
            self.l_name = self.user.last_name
        
        super(UserProfile, self,).save(force_insert, force_update)