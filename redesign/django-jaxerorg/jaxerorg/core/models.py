from datetime import date, datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import AutoSlugField
from sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.auth.models import User


class HomePageItem(models.Model):
    '''
        These items are displayed in the 6 primary slots of the homepage
        optionally, each item can be associated with a page/item around the site
        this will turn the title of the item into a link which will take the 
        user to the associated page.
    '''

    content_type =   models.ForeignKey(ContentType)
    object_id =      models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')    

    title = models.CharField(max_length=10, blank=False)
    description = models.CharField(max_length=20, blank=False)
    icon =  models.ImageField("Icon", upload_to="icons",
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
        
class HomeScrollPaneItem(models.Model):
    '''items for the scrolling panel on the home page.
       small class, but easy way to keep the site upto date'''
       
    text = models.CharField(max_length=15, blank=False)
    date_added = models.DateField(default=date.today()) 
    
class StandardContentItem(models.Model):
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
    slug = AutoSlugField(populate_from=('title','id'))
    description = models.CharField(max_length=255)
    date_posted = models.DateTimeField(default=datetime.now())
    date_modified = models.DateTimeField(default=datetime.now())
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
                                               'feature':{'size':(150,65),
                                                          'options':['crop']},
                                               'smallbox': {'size': (150, 150)},
                                               'headlines':{'size':(150,150)},
                                               'medium':{'size':(280,200)},
                                               'blog_manager':{'size':(215,150),
                                                                'quality':70,
                                                                'options':['crop']}
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
    def get_ct(self):
        return ContentType.objects.get_for_model(self)
    def get_ct_id(self):
        ''' returns the ID of this objects ContentType'''
        app = self.__module__.split('.')[-2]
        mod = self.__class__.__name__.lower()
        return ContentType.objects.get(app_label=app, model=mod).id
    
    class Meta:
        abstract=True
        ordering=['date_posted',]
