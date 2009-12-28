from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models import permalink
from django.contrib.auth.models import User
from diff_match_patch.diff_match_patch import diff_match_patch
from jaxerdoc.managers import Manager, CustomObjectManager, GlobalFunctionManager, UnmanagedQueItemManager
from jaxerorg.core.models import JaxerRelease
from jaxerhotsauce.models import ChangeSet
from jaxerutils.models import SelfAwareModel
import datetime

jsobjects = Q(model__iexact = 'javascriptobject')
jsfunction = Q(model__iexact = 'function')
jsclass = Q(model__iexact = 'classitem')
jsnamespace = Q(model__iexact = 'jaxernamespace')
MODERATION_OPTIONS = (
    ('approval', 'Approve'),
    ('denial', 'Deny')
)

class FunctionalityGroup(models.Model):
    ''' 
        Functionality groups are a broad way to classify the modules of jaxer
        Because so many different objects can fall into a single category
        doing related lookups from a category will be much easier that 
        trying to complile a list of different models who share the same
        grouped

        This is a convienece model. 
    '''
    title = models.CharField(_('Title'), max_length = 100,
                                      unique = True, blank = False)
    description = models.TextField(_('Description'), blank = False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('title',)  
        
    def __unicode__(self):
        return self.title           
class StandardDocumentModel(SelfAwareModel):
    '''
        The standard document is self away and expects to have a 
        generic relations to a ChangeSet Model via jaxerhotsauce
    '''
    editor = models.ForeignKey(User)
    name = models.CharField(_('Name'), max_length = 40, 
                            blank = False, unique = False)
    slug = models.CharField(max_length = 255, editable = False)          
    content = models.TextField(_('Content'), 
                               blank = False, 
                               help_text = 'This will be main content for the document page')
    # Saved content comes in as HTML text, but we don't want to index html
    # text. When saved, html tags will be stripped and a diference patch will
    # be saved.
    #
    # content the plain text is then saved and indexed by Xapian.
    html_patch = models.TextField(blank = True, 
                                  null = True, 
                                  editable = False)
    
    client_side = models.BooleanField()
    server_side = models.BooleanField()   
     
    on_line = models.BooleanField()
    changes = generic.GenericRelation(ChangeSet)    
    
    class Meta:
        abstract = True      
        
    def save(self, force_insert = False, force_update = False):
        try:
            self.slug = self.__unicode__().replace('.', '-')
        except:
            from django.template.defaultfilters import slugify
            self.slug = slugify(self.name)
        self.make_indexable()
        
        super(StandardDocumentModel, self).save(force_insert, force_update)
        
    def revert_to(self, revision, author = None):
        '''
        takes a revision number queries for the changset and returns it 
        '''
        
        #a ChangeSet Instance
        changeset = self.changes.get(version = revision)
        changeset.reapply(author)
        
    def preview_at(self, version):
        changeset = self.changes.get(revision = version)
        return changeset.see_item_at_version(version)     
    def latest_changeset(self):
        '''DOCSTRINGS'''
        try:
            return self.changes.order_by('-revision')[0]
        except:
            return ChangeSet.objects.none()
    def current_version(self):
        '''DOCSTRINGS'''
        return self.changeset_set.latest()[0]
    def get_latest_editor(self):
        try:
            editor = self.changes.latest().editor
        except:
            editor = self.editor
        return editor
    def version_number(self):
        count = self.changes.count()
        if count < 1:
            return 1
        else:
            return count    
    
    def apply_patch_from_que(self, ptext, description, editor):
        #will be betting a patch_text object from the queue
        #convert to actual patch
        #apply patch to object
        #save object

        DMP = diff_match_patch()
        patch = DMP.patch_fromText(ptext)
        self.description = DMP.patch_apply(patch, self.content[0])
        
    def make_new_revision(self, old_content, old_name, comment, editor):
        '''
            Function to be overridden
            
            This is the function that is called from the form that 
            is responsible for saving and editable item.
            
            This creates a new ChangeSet related to the object that called
            this function
        '''
        from jaxerhotsauce.utils import make_difPatch
        diff_text = make_difPatch(self.get_html_content(), old_content)
        change = ChangeSet.objects.create(content_diff = diff_text,
                                      content_type = self.get_ct(),
                                      object_id = self.id,
                                      comment = comment,
                                      old_name = old_name,
                                      editor = editor)
        return change
    def make_indexable(self):
        '''
            Incoming content is assumed to be HTML
            We want to index plain text, not html
            
            If the current content is already plain text, 
            we don't do anything
            
            else convert the html to plain text make 
            a patch to convert the text back to html
            save the plain text, save the patch as 
            text string save the object 
        '''
        from django.template.defaultfilters import striptags
        DMP = diff_match_patch()
        html = self.content
        plain_text = striptags(html)
        
        if not self.content == plain_text:
            patch = DMP.patch_make(plain_text, html)
            self.content = plain_text
            self.html_patch = DMP.patch_toText(patch)
             
    def get_html_content(self):
        if self.html_patch is None:
            return self.content
        else:
            DMP = diff_match_patch()
            patch = DMP.patch_fromText(self.html_patch)
            return DMP.patch_apply(patch, self.content)[0]
      
class Property(StandardDocumentModel):
    ''' properties are non-executable object associated with objects
        be aware that a property can be any object type, including
        another object which may also have properties.
    '''
    content_type = models.ForeignKey(ContentType, related_name = 'propparent')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    #what type of object is this property
#    js_type = models.ForeignKey(ContentType, related_name = 'propertytype')
#    js_id = models.PositiveIntegerField()
#    property_object = generic.GenericForeignKey('js_type', 'js_id')
#    properties = generic.GenericRelation('Property')
    
    # if a property may be an object which could also have properties! 
    properties = models.ManyToManyField('Property', blank = True, null = True)
    required = models.BooleanField()

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
            
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return ""          
    def type(self):
        return self.property_object
    def has_properties(self):
        return self.properties.count() > 0    
  
#generic can go on anything
class Parameter(StandardDocumentModel):
    '''
        Parameters are accepted by functions.
        they can be any javascript object or a Function
    '''
    #for ease of use
    
    # the type of parameter a function expects can
    # be just about anything
    js_type = models.ForeignKey(ContentType, 
                                limit_choices_to = Q(jsobjects | jsfunction))
    js_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('js_type', 'js_id')
    properties = models.ManyToManyField(Property, 
                                        related_name = "parameterproperty_set", 
                                        blank = True,
                                        null = True)
    required = models.BooleanField(_('Required'), 
                                   help_text = _('Is the parameter required?'))
    
    #the object this parameter is associated with
    content_type = models.ForeignKey(ContentType, 
                                     blank = True, 
                                     null = True, 
                                     related_name = 'to_function', 
                                     limit_choices_to = Q(jsobjects | jsfunction | jsclass))
    object_id = models.PositiveIntegerField(blank = True, null = True)    
    function_object = generic.GenericForeignKey('content_type', 'object_id')
    
    #
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return ""
    def has_properties(self):
        return self.properties.count() > 0
class Function(StandardDocumentModel):
    ''' 
        Functions should be attached to any JavaScriptObject or any thing'
        that subclasses a JavaScript Object ( Class, NameSpace)
        
        Functions do not need to be attached to another object. In this
        case they would be considered global functions
    '''
    example_code = models.TextField(blank = True, null = True)
    availablity = models.ForeignKey(JaxerRelease, 
                                    blank = True, 
                                    null = True, 
                                    related_name = "available_in")
    
    is_depricated = models.BooleanField()
    depricated = models.ForeignKey(JaxerRelease, 
                                   blank = True, 
                                   null = True, 
                                   related_name = "deripacted_in")

    is_global = models.BooleanField(_('Global'), 
                                    help_text = "is this a global function?")
    # this defines the object the function belongs to
    # a function does not have to belong to anything
    # it can be annonymous 
#    content_type = models.ForeignKey(ContentType, blank = True, null = True, related_name = 'parentobject')
#    object_id = models.PositiveIntegerField(blank = True, null = True)    
#    content_object = generic.GenericForeignKey('content_type', 'content_object')

    # the type of data a function returns
    # this can be any javascript object or another function
    # it does not have to return anything ( void )
    return_param = models.CharField(_('Variable Name'), max_length = 50,
                                     blank = True, null = True)
    return_type = models.ForeignKey(ContentType, blank = True,
                                      null = True, related_name = 'returntype')
    
    type_id = models.PositiveIntegerField(_("Object's ID"), blank = True, null = True)
    return_object = generic.GenericForeignKey('return_type', 'type_id') 
    returns = generic.GenericRelation('JavascriptObject')
    # parameters which make up the function signature
    parameters = models.ManyToManyField(Parameter, 
                                        related_name = 'functionparameter_set', 
                                        blank = True, 
                                        null = True)
    admin_objects = Manager()
    objects = GlobalFunctionManager()
    class Meta:
        verbose_name = "Function"      
    def __unicode__(self):
        return '%s' % self.name
    def get_absolute_url(self):
        return ""
    def get_return_vars(self):
        pass
 
# to be sub classed
class JavascriptObject(StandardDocumentModel):
    '''
        Representation of the JavaScript Object
        Naitive objects would be Array, String
    '''
    # the generic relation of the object is primarily for functions that return more than 1 object
    content_type = models.ForeignKey(ContentType, 
                                blank = True, 
                                null = True, 
                                related_name = 'returnobject_set')
    object_id = models.PositiveIntegerField(blank = True, null = True)    
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    #for use with inline models only
    ret_obj_type = models.ForeignKey(ContentType, 
                                     blank = True, 
                                     null = True, 
                                     related_name = 'returntype_set', 
                                     limit_choices_to = Q(jsobjects | jsclass | jsnamespace))
    ret_obj_id = models.PositiveIntegerField(blank = True, null = True)    
    ret_object = generic.GenericForeignKey('ret_obj_type', 'ret_obj_id')

    naitive = models.BooleanField(help_text =_('Is this a naitive JS Object?'))
    properties = models.ManyToManyField(Property, blank = True, null = True)
    methods = models.ManyToManyField(Function, blank = True, null = True)     
#   admin_objects =  NaitiveObjectManager()
    objects = Manager()
    class Meta:
        verbose_name = 'Object'    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return ""        
    def type(self):
        return "Object"
    def has_properties(self):
        return self.properties.count() > 0
    def has_methods(self):
        return self.methods > 0
class JaxerNameSpace(JavascriptObject):
    #this is a subclass used to organize Jaxer's Namespace Objects
    #apart from the Standard javascript Objects(String, Array, etc)
    root_namespace = models.ForeignKey('self', blank = True,
                                         null = True, related_name = 'rootnamespace',
                                         help_text = 'This should almost always be the Jaxer Namespace')
    parent_namespace = models.ForeignKey('self', 
                                         blank = True, 
                                         null = True)
    category = models.ForeignKey(FunctionalityGroup, blank = True, null = True)    
    search_name = models.CharField(max_length = 150, 
                                   editable = False, blank = True)
    objects = CustomObjectManager()
    availablity = models.ForeignKey(JaxerRelease, 
                                    blank = True, 
                                    null = True, 
                                    related_name = "ns_available")
    depricated = models.ForeignKey(JaxerRelease, 
                                   blank = True, 
                                   null = True, 
                                   related_name = "ns_deripacted")
    is_depricated = models.BooleanField()   
    
    class Meta:
        verbose_name = "Namespace"
        
    def __unicode__(self):
        if self.root_namespace and self.parent_namespace :
            return ".".join([self.root_namespace.name, self.parent_namespace.name, self.name])
        elif self.root_namespace is None and self.parent_namespace is not None:
            return ".".join([self.parent_namespace.name, self.name])
        elif self.root_namespace is not None and self.parent_namespace is None:
            return ".".join([self.root_namespace.name, self.name])
        else:
            return "%s" % self.name
        
    @permalink
    def get_absolute_url(self):
        return('jaxerdoc.views.document_detail', (), {'oslug':self.slug, 
                                                      'ctid':self.get_ct_id(), 
                                                      'objid':self.id})
        
    def save(self, force_insert = False, force_update = False):
        self.search_name = self.__unicode__()
        super(JaxerNameSpace, self).save(force_insert, force_update)   
        
class ClassItem(StandardDocumentModel):
    
    '''
       ClassItem reprsents class which resideds inside of a namespace
       the name classitem was used to prevent naming conflicts
       
       Javascript does not have classes, they are actually functions
       We cannot subclass the Function class, as it would violate
       django's DB contstraints setup
       Treated as objects - 
    '''
    namespace = models.ForeignKey(JaxerNameSpace)
    example_code = models.TextField(blank = True, null = True)
    availablity = models.ForeignKey(JaxerRelease, blank = True, null = True, related_name = "classavailability")
    
    is_depricated = models.BooleanField()
    depricated = models.ForeignKey(JaxerRelease, blank = True, null = True, related_name = "classdeprication")
    parameters = models.ManyToManyField(Parameter, related_name = 'classparameter_set', blank = True, null = True)
    methods = models.ManyToManyField(Function, related_name = "classmethod_set", blank = True, null = True)  
    properties = models.ManyToManyField(Property, related_name = "classproperty_set", blank = True, null = True)
    search_name = models.CharField(max_length = 150, editable = False, blank = True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
            
    def __unicode__(self):
        return ".".join([self.namespace.__unicode__(), self.name])    
    @permalink
    def get_absolute_url(self):
        return('jaxerdoc.views.document_detail', (), {'oslug':self.slug, 'ctid':self.get_ct_id(), 'objid':self.id})
    def save(self, force_insert = False, force_update = False):
        self.search_name = self.__unicode__()
        super(ClassItem, self).save(force_insert, force_update)    
    def class_name(self):
        return self.__unicode__()
    def type(self):
        return "%s Instance" % self.__unicode__()
    def has_properties(self):
        return self.properties.count() > 0
    def has_methods(self):
        return self.methods.count() > 0
    def has_parameters(self):
        return self.parameters.count() > 0
    
# the queueditem is the crux of the documentation
# it is how both users and moderators dictate the advancement,
# editing, creation and moderation of the docs.
class QueuedItem(models.Model):
    ''' 
        The queueditem is the crux of the wiki system within jaxerdoc.
        This model stores the data about items that have been edited
        or in the event someone wishes to add new content, the QueuedItem
        will hold the data about the propsed object and the object it is to
        be associated with until the new object is/is not created.
    
        when the body of a document is edited, we do not want to to go
        live on the site. The QueuedItem model is a generic item that
        holds a reference to: 
        
        the item that was edited
        the current revision of the reverence item 
        ( incase an edit is accepted after this was submitted )
        
        The content as is ( HTML CODE INCLUDED )
        
        This is really only for editing the main body of a document.
    '''
    ACTION_FLAGS = (
        ('edit', 'Edit'),
        ('new', 'Create')
    )
    editor = models.ForeignKey(User)
    ############################################################
    # this is the direct link to the object that this queue item
    # is associated with
    content_type = models.ForeignKey(ContentType, blank = True, null = True)
    object_id = models.PositiveIntegerField(blank = True, null = True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    ############################################################
    submit_date = models.DateTimeField(_('Submitted'), default = datetime.datetime.now(), editable = False)
    content = models.TextField(blank = True, null = True)
    at_revision = models.PositiveIntegerField()
    
    # edit/create flag
    action = models.CharField(max_length = 40, choices = ACTION_FLAGS,
                                        blank = False, null = False)
    
    # if we are going to let users create new objects, we need to know what 
    # they are creating ( by type )
    # we don't want an id number or generic FK becuase the object 
    # will not exist until we approve the creation of it.
    add_title = models.CharField(max_length = 200, blank = True)
    adding_type = models.ForeignKey(ContentType, blank = True, null = True, related_name = "linkedobject")
    add_summary = models.TextField(_('Summary'), help_text = "What/why should we add this?", blank = True)
    
    # security hash. If a new object is accepted, the item will be blank
    # we want to give the user a chance to fill in the page before it goes live
    # we will create a key and mail it to the user giving them a link
    # to the page where they are allowed to do 1 edit/save
    add_key = models.CharField(max_length = 300, editable = False, blank = True, null = True)
    key_expired = models.BooleanField(editable = False)
    comment = models.CharField(max_length = 400, blank = True)

    moderate = models.CharField(max_length = 30, choices = MODERATION_OPTIONS,
                                                      blank = True, null = True)
    mod_reason = models.CharField(_('Mod Comments'), max_length = 300, blank = True, null = True)
    objects = Manager()
    unmanaged = UnmanagedQueItemManager()
    
    class Meta:
        ordering = ('submit_date',)
        permissions = (
               ('can_moderate_docs', 'Can Moderate Docs'),
        )    
    def save(self, force_insert = False, force_update = False):
        
        super(QueuedItem, self).save(force_insert, force_update)
    def __unicode__(self):
        return "edit for %s on revision %s" % (self.content_object, self.at_revision)
    def review_content(self):
        return self.content_object.preview_at(self.at_revision)
    def display_diff_html(self):
        # get the content object's HTML
        # get all of its changesets greater than this version number
        # aplly the patches ( do not save over )
        # get difference HTML between the reverted object ( if reverted )
        # return the content object HTML( original )
        # return the difference HTML
        
        dmp = diff_match_patch()
        document_obj = self.content_object
        
        #get all changesets greater than self.revision ordered -revision
        changesets = document_obj.changes.filter(revision__gt = self.at_revision
                                                 ).order_by('-revision') or None
        
        #collect the content diff & convert to patch
        current_html = None
        if changesets is not None:
            for change in changesets:
                if current_html is None:
                    current_html = document_obj.get_html_content()
                    
                patch = dmp.patch_fromText(change.content_diff)
                
                #apply patches to the current content object
                current_html = dmp.patch_apply(patch, current_html)[0]
        else:
            current_html = document_obj.get_html_content()
        diffs = dmp.diff_main(current_html, self.content, checklines = False)
        return dmp.diff_prettyHtml(diffs)
    def is_moderated(self):
        return not self.moderate == None
    
    def get_activation_key(self):
        if self.action == 'new' and self.moderate == "approval":
            from hashlib import sha224
            secure_string = '$sha$%s$%s$%s' % (self.adding_type, self.editor.username, self.created)
            return sha224(secure_string).hexdigest()
        else:
            return None
    def is_new_item(self):
        return self.action == 'new'
