from datetime import date, datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import AutoSlugField
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.auth.models import User
from jaxerutils.models import SelfAwareModel

OS_OPTIONS=(
   ('Windows',(
        ('.zip', 'Windows XP/Vista'),
        ('.zip', 'Windows 7'),
      )
   ),
   ('Linux 32 Bit',(
        ('.tar.gz','Linux'),
      )  
    ),
    ('Linux 64 Bit',(
        ('.tar.gz', 'Linux'),
      )  
    ),
    ('Mac', ( 
        ('.dmg','Mac OS X'),
      )  
    )
)
RELEASE_STATE=(
    ('beta', 'Beta'),
    ('alpha', 'Alpha'),
    ('stable', 'Stable'),
    ('insecure', 'Insecure')
)
class HomePageItem(SelfAwareModel):
    '''
        These items are displayed in the 6 primary slots of the homepage
        optionally, each item can be associated with a page/item around the site
        this will turn the title of the item into a link which will take the 
        user to the associated page.
    '''

    content_type =   models.ForeignKey(ContentType, blank=True, null=True)
    object_id =      models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')    

    title = models.CharField(max_length=10, blank=False)
    description = models.CharField(max_length=255, blank=False)
    icon =  models.ImageField(_("Icon"), upload_to="icons", blank=False, null=False,
                          help_text="A transparent PNG file maximum size 50x50"
                         )
    def __unicode__(self):
        return "%s" % self.title
    
    def __str__(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        try:
            return self.content_object.get_absolute_url()
        except:
            return "#"
        
    class Meta:
        verbose_name="Home Page Item"
        verbose_name_plural="Home Page Items"
        get_latest_by = "created"
        
class HomeScrollPaneItem(models.Model):
    '''items for the scrolling panel on the home page.
       small class, but easy way to keep the site upto date'''
       
    text = models.CharField(max_length=15, blank=False)
    date_added = models.DateField(default=date.today()) 
           
class StandardContentItem(SelfAwareModel):
    """
        this is the site's baisc content item. It will allow for easy updates
        However, there is no version control added.
        Good for pages that may not change much and will save on DB overhead
        with out the addition of changesets.
    """
    
    DOCUMENT_STATUS=(
        (1, 'Draft'),
        (2, 'Awaiting Edit'),
        (3, 'Awaiting Proof'),
        (4, 'Published'),
        (5, 'Archived')
    )
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title')
    description = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField('Status', choices=DOCUMENT_STATUS)
    hits = models.PositiveIntegerField(default=0, editable=False)
    allow_comments = models.BooleanField(blank=True)
    #additional sizes can be addeed to extra_thumbnails at anytime
    display_image = ImageWithThumbnailsField(upload_to='images/',
                                             default="", 
                                             thumbnail={'size':(80, 80)},
                                             extra_thumbnails={
                                               'icon': {'size': (45, 45)},
                                               'thumb': {'size': (80, 80)},
                                               'feature':{'size':(150,65), 'options':['crop']},
                                               'smallbox': {'size': (150, 150)},
                                               'headlines':{'size':(150,150)},
                                               'medium':{'size':(280,200)},
                                               'blog_manager':{'size':(215,150),
                                                                'quality':70, 'options':['crop']}
                                                }
                                             )
    was_published = models.BooleanField(blank=True, editable=False)
    
    def __unicode__(self):
        return "%s" % self.title
    
    def __str__(self):
        return self.__unicode__()
    
    def viewed(self):
        self.hits += 1
        self.save()
    def is_published(self):
        '''check to see if the current item is published'''
        return self.status == 4
    def has_been_published(self):
        '''check to see if the item has ever been published'''
        return self.was_published
    def comments_enabled(self):
        '''check to see if comments are enabled for this item'''
        return self.comments_enabled

    class Meta:
        abstract=True
        ordering=['date_posted',]
        
class DownloadableFile(SelfAwareModel):
    download=     models.FileField(upload_to='doanloads/')
    date_released = models.DateField(blank=False, default=datetime.now())
    content_type = models.ForeignKey(ContentType)
    object_id =    models.PositiveIntegerField(default=0)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    class Meta:
        abstract = True
        ordering =['-date_released',]

class JaxerDownload(DownloadableFile):
    os =       models.CharField(max_length=100, choices=OS_OPTIONS)
    comment =  models.CharField(max_length=255, blank=True)    

class JaxerRelease(SelfAwareModel):
    
    name =     models.CharField(max_length=255)
    
    major =    models.PositiveSmallIntegerField(default=0)
    minor =    models.PositiveSmallIntegerField(default=0)
    security = models.PositiveSmallIntegerField(default=0)
    bug_fix =  models.PositiveIntegerField(default=0)
    
    notes =    models.TextField()
    
    development = models.BooleanField(_('Development Version')) 
    release_date = models.DateField(_("Release Date"))
    downloads = generic.GenericRelation(JaxerDownload)
    def __unicode__(self):
        return '%s %s' % (self.name, self.get_version())
    def get_version(self):
        version =""
        if self.bug_fix > 0:
            version = ".".join(['%s', '%s', '%s', '%s'])%(self.major, self.minor, self.security, self.bug_fix)
        elif self.security > 0:
            version =".".join(['%s', '%s', '%s'])%(self.major, self.minor, self.security)
        else:
            version = "%s.%s" % (self.major, self.minor)
        return version
    
    def get_short_version(self):
        return "%s.%s" % (self.major, self.minor)
        
    class Meta:
        pass
class Article(StandardContentItem):
    pass
    class Meta:
        pass