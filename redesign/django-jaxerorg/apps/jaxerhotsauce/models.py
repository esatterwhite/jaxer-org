''' Wiki Models '''
from django.db import models
from django.contrib.admin.models import User
from diff_match_patch import diff_match_patch
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
#from django.contrib import contenttypes 
from datetime import datetime
from django.db.models import Manager
from django_extensions.db.fields import AutoSlugField
# Create your models here.

#diff_match_patch instance
DMP = diff_match_patch.diff_match_patch()
class ChangeSet(models.Model):
    ''' 
        The ChangeSet can be attached to any object and
        
        ment to be connected to a Class which subclases
        EditableItem as a generic inline relation
        
        import this in to your application's admin.py
        create a generic inline and attach it to anything
        which subclasses EditableItem as a generic inline
        and you have a "wiki-able" item
    '''
    content_type =   models.ForeignKey(ContentType)
    object_id =      models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')    
    editor =         models.ForeignKey(User, limit_choices_to={'is_staff':True})
    revision =       models.PositiveIntegerField()   
    comment =        models.CharField(max_length=255, blank=True, help_text="Tell us why/what you are changing")
    content_diff =   models.TextField('Content Patch', editable=False, blank=True)
    date_modified =  models.DateTimeField(default = datetime.now(), blank=False)
    old_name =       models.CharField("Name", max_length = 255, blank = True)
    
    approve_change = models.BooleanField()
    deny_change =    models.BooleanField()
    
    objects =        Manager()
    class Meta:
        ordering = ('-revision', )
        get_latest_by = 'date_modified'
               
    def __unicode__(self):
        return "revision %s" % self.revision
    def see_item_at_version(self, version):
        ''' reverts the content of the object and returns it with out saving'''
        editable_object = self.content_object
        #get all changesets greater than self.revision ordered -revision
#        if version == 1:
#            changesets = editable_object.changes.filter(
#                                                      revision__gte=self.revision
#                                                      ).order_by('-revision')
#        else:
        changesets = editable_object.changes.filter(
                                                      revision__gte=self.revision
                                                      ).order_by('-revision')
        
        #collect the content diff & convert to patch
        content = None
        for change in changesets:
            if content is None:
                content = editable_object.get_html_content()              
            patch = DMP.patch_fromText(change.content_diff)           
            #apply patches to the current content object
            content = DMP.patch_apply(patch, content)[0]
        return content  
    def reapply(self, editor):
        ''' 
            apply the patch to the content_object
            which will always be an EditableItem
        '''
        #get content object
        editable_object = self.content_object
               
        #get all changesets greater than self.revision ordered -revision
        changesets = editable_object.changes.filter(
                                                      revision__gt=self.revision
                                                      ).order_by('-revision')
        
        #collect the content diff & convert to patch
        content = None
        for change in changesets:
            if content is None:
                content = editable_object.body
                
            patch = DMP.patch_fromText(change.content_diff)
            
            #apply patches to the current content object
            content = DMP.patch_apply(patch, content)[0]
            change.reverted = True
            change.save()
            
        old_content = editable_object.body
        old_title = change.title
        
        editable_object.body = content
        editable_object.save()
        editable_object.make_new_revision(old_content, 
                                          old_title, 
                                          comment="Reverted to revision %s" % self.revision, 
                                          editor=editor)
    def apply_queued_diff(self, cs):
        patch_text = cs.content_diff
        patch = DMP.patch_fromText()
        new_version = DMP.patch_apply(patch, patch_text)
        self.content_object.description = new_version
        try:
            self.revision = ChangeSet.objects.filter(content_type=self.content_type, object_id = self.content_object.id).latest().revision +1
        except:
            self.revision = 1
        self.save()
        self.content_object.save()
    def display_change_html(self):
        ''' return the html string of a changeset'''
        old_content = self.content_object.content
        newer_changesets = ChangeSet.objects.filter(content_type=self.content_type,
                                                    object_id=self.content_object.id,
                                                    revision__gte=self.revision)
        for i, changeset in enumerate(newer_changesets):
            patches = DMP.patch_fromText(changeset.content_diff)
            
            if len(newer_changesets)==i+1:
                next_rev_content = old_content
            old_content = DMP.patch_apply(patches, old_content)[0]
        
        diffs = DMP.diff_main(old_content, next_rev_content, checklines=False)
        return DMP.diff_prettyHtml(diffs)
    
    def save(self, force_insert=False, force_update=False):
        ''' overridden save method'''
        try:
            self.revision = ChangeSet.objects.filter(content_type=self.content_type, object_id = self.content_object.id).latest().revision +1
        except:
            self.revision = 1
        super(ChangeSet, self).save(force_insert, force_update)

    
    content_type = models.ForeignKey(ContentType)
    object_id =    models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
class EditableItem(models.Model):
    ''' 
        base item for wiki. only field is main editable content
        we want to version
        
        This can be imported into any application that wishes
        to maintain a version log
    '''
    title = models.CharField('Title', max_length=255)
    slug =  AutoSlugField(populate_from=('title'), unique=True,help_text="A Slug is a URL friendly phrase for identifying objects.\
                                                This will be formulated for you")    
    content =   models.TextField('Editable Content')
    author =    models.ForeignKey(User)
    date_created = models.DateTimeField('Creation Date', default=datetime.now)
    date_modified = models.DateTimeField(
                                         default=datetime.now, 
                                         auto_now=True, 
                                         editable=False
                                         )
    class Meta:
        abstract = True

    def revert_to(self, revision, author=None):
        '''takes a revision number queries for the changset and returns it '''
        
        #a ChangeSet Instance
        changeset = self.changeset_set.objects.get(version=revision)
        changeset.reapply(author)
        
    def latest_changeset(self):
        '''DOCSTRINGS'''
        try:
            return self.changes.order_by('-revision')[0]
        except:
            return ChangeSet.objects.none()
    def current_version(self):
        '''DOCSTRINGS'''
        return self.changeset_set.latest()[0]
    def make_new_revision(self, old_content, old_title, comment, editor):
        '''
            Function to be overridden
            
            This is the function that is called from the form that 
            is responsible for saving and editable item.
            
            This creates a new ChangeSet related to the object that called
            this function
        '''
        from jaxerhotsauce.utils import make_difPatch
        diff_text = make_difPatch(self.content, old_content)
        change = ChangeSet.objects.create(content_diff=diff_text, 
                                      content_type=self.content_type, 
                                      object_id=self.id, 
                                      comment=comment,
                                      old_title=old_title,
                                      editor=editor)
        return change
    
    def get_ct(self):
        ''' returns the ID of this objects ContentType'''
        return ContentType.objects.get_for_model(self)
        