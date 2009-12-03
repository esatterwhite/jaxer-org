from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.db.models import permalink
from jaxerorg.core.models import JaxerRelease
from jaxerhotsauce.models import ChangeSet
from django.contrib.auth.models import User
from diff_match_patch.diff_match_patch import diff_match_patch
from jaxerdoc.managers import Manager, NaitiveObjectManager, CustomObjectManager, GlobalFunctionManager
import datetime

jsobjects =       Q(model__iexact='javascriptobject')
jsfunction =      Q(model__iexact='function')
jsclass =         Q(model__iexact='classitem')
jsnamespace =     Q(model__iexact='jaxernamespace')

# generic - can go on anything
class SelfAwareModel(models.Model):
    '''
        An Abstract model: models which subclass the SelfAwareModel
        will have a series of methods that give quick access to that
        model's meta information:
        
        Content Type & it's ID
        App Label
        Model Name
        Class Name
        
        The aim is to make working with generic models easier from a
        template as generic relations offer a good deal of information
        about the related object, but accessing information about the 
        target object/model itself can be frustrating.
        
        Way to add Standarized functionality with out changing model strucure
    '''
    def get_ct(self):
        return ContentType.objects.get_for_model(self)
    
    def get_ct_id(self):
        return self.get_ct().id
    
    def get_app_label(self):
        return self.get_ct().app_label
    
    def get_model_name(self):
        return self.get_ct().model
    
    def get_class_name(self):
        return self._meta.verbose_name
        
    class Meta:
        abstract = True    
        
class StandardDocumentModel(SelfAwareModel):
    '''
        The standard document is self away and expects to have a 
        generic relations to a ChangeSet Model via jaxerhotsauce
    '''
    editor =         models.ForeignKey(User)
    name =           models.CharField(_('Name'), max_length=40, blank=False, unique=False)
    slug =           models.CharField(max_length=255, editable=False)          
    content =        models.TextField(_('Content'), blank=False, help_text='This will be main content for the document page')
    date_modified =  models.DateTimeField(default=datetime.datetime.now(), auto_now=True, editable=False)
    # Saved content comes in as HTML text, but we don't want to index html
    # text. When saved, html tags will be stripped and a diference patch will
    # be saved.
    #
    # content the plain text is then saved and indexed by Xapian.
    html_patch =     models.TextField(blank=True, null=True, editable=False)
    
    
    client_side =    models.BooleanField()
    server_side =    models.BooleanField()   
     
    on_line =        models.BooleanField()
    changes =        generic.GenericRelation(ChangeSet)    
    
    
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
        change =    ChangeSet.objects.create(content_diff=diff_text, 
                                      content_type=self.content_type, 
                                      object_id=self.id, 
                                      comment=comment,
                                      old_name=old_name,
                                      editor=editor)
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
        from         django.template.defaultfilters import striptags
        DMP =        diff_match_patch()
        html =       self.content
        plain_text = striptags(html)
        
        if not self.content == plain_text:
            patch =           DMP.patch_make(plain_text, html)
            self.content =    plain_text
            self.html_patch = DMP.patch_toText(patch)
             
    def get_html_content(self):
        if self.html_patch is None:
            return self.content
        else:
            DMP = diff_match_patch()
            patch = DMP.patch_fromText(self.html_patch)
            return DMP.patch_apply(patch, self.content)[0]
    def save(self, force_insert=False, force_update=False):
        try:
            self.slug = self.__unicode__().replace('.','-')
        except:
            from django.template.defaultfilters import slugify
            self.slug = slugify(self.name)
        self.make_indexable()
        
        super(StandardDocumentModel,self).save(force_insert, force_update)
        
    class Meta:
        abstract = True
class JaxerCodeSnippet(SelfAwareModel):
    '''code class'''
    author =         models.ForeignKey(User)
    code =           models.TextField()  
    content_type =   models.ForeignKey(ContentType)
                    
class Property(StandardDocumentModel):
    '''property class'''
    content_type =    models.ForeignKey(ContentType, related_name='propparent')
    object_id =       models.PositiveIntegerField()
    content_object =  generic.GenericForeignKey('content_type', 'content_object')
    
    #what type of object is this property
    prop_type =       models.ForeignKey(ContentType, related_name='propertytype')
    prop_id =         models.PositiveIntegerField()
    property_object = generic.GenericForeignKey('prop_type', 'prop_id')
    required =        models.BooleanField()
    def __unicode__(self):
        return self.name
    def type(self):
        return self.property_object
    class Meta:
        verbose_name =        "Property"
        verbose_name_plural = "Properties"
    def get_absolute_url(self):
        return ""        
#generic can go on anything

class Parameter(StandardDocumentModel):
    '''
        Parameters are accepted by functions.
        they can be any javascript object or a Function
    '''
    #for ease of use
    
    # the type of parameter a function expects can
    # be just about anything
    param_type =      models.ForeignKey(ContentType, limit_choices_to=Q(jsobjects|jsfunction))
    param_id =        models.PositiveIntegerField()
    content_object =  generic.GenericForeignKey('param_type', 'param_id')
    properties =      generic.GenericRelation(Property)
    required =        models.BooleanField(_('Required'), help_text=_('Is the parameter required?'))
    
    #the object this parameter is associated with
    content_type =    models.ForeignKey(ContentType,blank=True, null=True, related_name='to_function', limit_choices_to=Q(jsobjects|jsfunction|jsclass))
    object_id =       models.PositiveIntegerField(blank=True, null=True)    
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
    example_code =   models.TextField(blank=True, null=True)
    availablity =    models.ForeignKey(JaxerRelease, blank=True, null=True, related_name="available_in")
    
    is_depricated =  models.BooleanField()
    depricated =     models.ForeignKey(JaxerRelease,blank=True, null=True, related_name="deripacted_in")

    is_global =      models.BooleanField(_('Global'), help_text="is this a global function?")
    # this defines the object the function belongs to
    # a function does not have to belong to anything
    # it can be annonymous 
    content_type =   models.ForeignKey(ContentType, blank=True, null=True, related_name='parentobject')
    object_id =      models.PositiveIntegerField(blank=True, null=True)    
    content_object = generic.GenericForeignKey('content_type', 'content_object')

    # the type of data a function returns
    # this can be any javascript object or another function
    # it does not have to return anything ( void )
    return_param =   models.CharField(_('Variable Name'), max_length=50, 
                                     blank=True, null=True)
    return_type =    models.ForeignKey(ContentType, blank=True, 
                                      null=True, related_name='returntype')
    
    type_id =       models.PositiveIntegerField(_("Object's ID"), blank=True, null=True)
    return_object = generic.GenericForeignKey('return_type','type_id') 
    returns =       generic.GenericRelation('JavascriptObject')
    # parameters which make up the function signature
    parameters =    generic.GenericRelation(Parameter)
    admin_objects = Manager()
    objects =       GlobalFunctionManager()
    
    def __unicode__(self):
        return '%s' % self.name
    def get_absolute_url(self):
        return ""
    def get_return_vars(self):
        pass
    class Meta:
        verbose_name = "Function"   
        
# to be sub classed
class JavascriptObject(StandardDocumentModel):
    '''
        Representation of the JavaScript Object
        Naitive objects would be Array, String
    '''
    # the generic relation of the object is primarily for functions that return more than 1 object
    content_type =   models.ForeignKey(ContentType, blank=True, null=True, related_name='returnobject_set')
    object_id =      models.PositiveIntegerField(blank=True, null=True)    
    content_object = generic.GenericForeignKey('content_type', 'content_object')

    #for use with inline models only
    ret_obj_type =   models.ForeignKey(ContentType, blank=True, null=True, related_name='returntype_set',limit_choices_to=Q(jsobjects|jsclass|jsnamespace))
    ret_obj_id =     models.PositiveIntegerField(blank=True, null=True)    
    ret_object =     generic.GenericForeignKey('ret_obj_type', 'ret_obj_id')

    naitive =        models.BooleanField(help_text=_('Is this a naitive JS Object?'))
    properties =     generic.GenericRelation(Property)
    methods =        generic.GenericRelation(Function)     
#   admin_objects =  NaitiveObjectManager()
    objects =        Manager()
    
    def get_absolute_url(self):
        return ""    
    class Meta:
        verbose_name = 'Object'
    def __unicode__(self):
        return self.name
    def type(self):
        return "Object"
    def has_properties(self):
        return self.properties.count() > 0
    def has_methods(self):
        return self.methods > 0
    
class JaxerNameSpace(JavascriptObject):
    #this is a subclass used to organize Jaxer's Namespace Objects
    #apart from the Standard javascript Objects(String, Array, etc)
    root_namespace =   models.ForeignKey('self', blank=True, null=True, related_name='rootnamespace')
    parent_namespace = models.ForeignKey('self', blank=True, null=True)
    search_name =      models.CharField(max_length=150, editable=False, blank=True)
    objects =          CustomObjectManager()
    availablity =      models.ForeignKey(JaxerRelease, blank=True, null=True, related_name="ns_available")
    depricated =       models.ForeignKey(JaxerRelease, blank=True, null=True, related_name="ns_deripacted")
    is_depricated =    models.BooleanField()   
    
    class Meta:
        verbose_name = "Namespace"
        
    def __unicode__(self):
        if self.root_namespace and self.parent_namespace :
            return ".".join([self.root_namespace.name,self.parent_namespace.name, self.name])
        elif self.root_namespace is None and self.parent_namespace is not None:
            return ".".join([self.parent_namespace.name, self.name])
        elif self.root_namespace is not None and self.parent_namespace is None:
            return ".".join([self.root_namespace.name, self.name])
        else:
            return "%s" % self.name
        
    @permalink
    def get_absolute_url(self):
        return('jaxerdoc.views.document_detail', (), {'oslug':self.slug, 'ctid':self.get_ct_id(), 'objid':self.id})
        
    def save(self, force_insert=False, force_update=False):
        self.search_name=self.__unicode__()
        super(JaxerNameSpace, self).save(force_insert, force_update)
        
class ClassItem(Function):
    
    '''
       ClassItem reprsents class which resideds inside of a namespace
       the name classitem was used to prevent naming conflicts
       
       Javascript does not have classes, they are actually functions
       Treated as objects - 
    '''
    namespace =   models.ForeignKey(JaxerNameSpace)
    methods =     generic.GenericRelation(Function, related_name='classmethods')  
    properties =  generic.GenericRelation(Property, related_name='classproperites')
    search_name = models.CharField(max_length=150, editable=False, blank=True)
    
    def __unicode__(self):
        return ".".join([self.namespace.__unicode__(), self.name])
    def class_name(self):
        return self.__unicode__()
    def type(self):
        return "%s Instance" % self.__unicode__()
    def has_properties(self):
        return self.properties.count() >0
    @permalink
    def get_absolute_url(self):
        return('jaxerdoc.views.document_detail', (), {'oslug':self.slug,'ctid':self.get_ct_id(), 'objid':self.id})
    
    def save(self, force_insert=False, force_update=False):
        self.search_name=self.__unicode__()
        super(ClassItem, self).save(force_insert, force_update)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        
class QueuedItem(models.Model):
    ''' when the body of a document is edited, we do not want to to go
        live on the site. The QueuedItem model is a generic item that
        holds a reference to: 
        
        the item that was edited
        the current revision of the reverence item 
        ( incase an edit is accepted after this was submitted )
        
        The content as is ( HTML CODE INCLUDED )
        
        This is really only for editing the main body of a document.
    '''
    content_type =   models.ForeignKey(ContentType)
    object_id =      models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    content =        models.TextField(blank=False)
    at_revision =    models.PositiveIntegerField()
    
    approve =        models.BooleanField()
    deny =          models.BooleanField()
    
    def __unicode__(self):
        return "edit for %s on revision %s" %(self.content_object, self.at_revision)
    def display_diff_html(self):
        # get the content object's HTML
        # get all of its changesets greater than this version number
        # aplly the patches ( do not save over )
        # get difference HTML between the reverted object ( if reverted )
        # return the content object HTML( original )
        # return the differenc HTML ( proposed Change )
        
        dmp = diff_match_patch()
        document_obj = self.content_object
        proposed_change = None
        
        #get all changesets greater than self.revision ordered -revision
        changesets = document_obj.changeset_set.filter(
                                                      revision__gt=self.at_revision
                                                      ).order_by('-revision')
        
        #collect the content diff & convert to patch
        current_html = None
        for change in changesets:
            if current_html is None:
                current_html = document_obj.get_html_content()
                
            patch = dmp.patch_fromText(change.content_diff)
            
            #apply patches to the current content object
            current_html = dmp.patch_apply(patch, current_html)[0]
            
        diffs = dmp.diff_main(current_html, proposed_change, checklines=False)
        return dmp.diff_prettyHtml(diffs)