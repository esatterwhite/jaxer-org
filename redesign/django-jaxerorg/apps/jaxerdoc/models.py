from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from jaxerdoc.managers import Manager, NaitiveObjectManager, CustomObjectManager, GlobalFunctionManager
from django.db.models import Q
from jaxerorg.core.models import JaxerRelease
from jaxerhotsauce.models import ChangeSet
from django.contrib.auth.models import User
from diff_match_patch.diff_match_patch import diff_match_patch
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
        return self.__class__.__name__
        
    class Meta:
        abstract = True    
        
class StandardDocumentModel(SelfAwareModel):
    '''
        The standard document is self away and expects to have a 
        generic relations to a ChangeSet Model via jaxerhotsauce
    '''
    editor =         models.ForeignKey(User)
    name =           models.CharField(_('Name'), max_length=40, blank=False, unique=True)
    content =        models.TextField(_('Description'), blank=False)
    
    # Saved content comes in as HTML text, but we don't want to index html
    # text. When saved, html tags will be stripped and a diference patch will
    # be saved.
    #
    # content the plain text is then saved and indexed by Xapian.
    html_patch =     models.TextField(blank=True, editable=False)
    
    
    client_side =    models.BooleanField()
    server_side =    models.BooleanField()   
     
    on_line =      models.BooleanField()
    changes =      generic.GenericRelation(ChangeSet)    
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
        diff_text = make_difPatch(self.content, old_content)
        change = ChangeSet.objects.create(content_diff=diff_text, 
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
            
            If the current content is already plain text, we don't do anything
            
            else convert the html to plain text
            make a patch to convert the text back to html
            save the plain text, save the patch as text string
            save the object 
        '''
        from django.template.defaultfilters import striptags
        DMP = diff_match_patch()
        html = self.content
        plain_text = striptags(html)
        
        if self.content == plain_text:
            return True
        else:
            patch = DMP.patch_make(plain_text, html)
            self.content = plain_text
            self.html_patch = DMP.patch_toText(patch)
            self.save()
             
    def get_html_content(self):
        DMP = diff_match_patch()
        patch = DMP.patch_fromText(self.html_patch)
        return DMP.patch_apply(patch, self.content)[0]
    
    class Meta:
        abstract = True
class JaxerCodeSnippet(SelfAwareModel):
    author =         models.ForeignKey(User)
    code =           models.TextField()
    
    content_type =   models.ForeignKey(ContentType)
                    
class Property(StandardDocumentModel):
    
    content_type = models.ForeignKey(ContentType, related_name='propparent')
    object_id =    models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'content_object')
    
    #what type of object is this property
    prop_type =      models.ForeignKey(ContentType, related_name='propertytype')
    prop_id =        models.PositiveIntegerField()
    property_object = generic.GenericForeignKey('prop_type', 'prop_id')
    
    def __unicode__(self):
        return self.name
    def type(self):
        return self.property_object
    class Meta:
        verbose_name =        "Property"
        verbose_name_plural = "Properties"
        
#generic can go on anything

class Parameter(StandardDocumentModel):
    '''
        Parameters are accepted by functions.
        they can be any javascript object or a Function
    '''
    #for ease of use
    jsobjects =       Q(model__iexact='javascriptobject')
    jsfunction =      Q(model__iexact='function')
    jsclass =         Q(model__iexact='classitem')
    
    # the type of parameter a function expects can
    # be just about anything
    param_type =      models.ForeignKey(ContentType, 
                                 limit_choices_to=Q(jsobjects|jsfunction))
    param_id =        models.PositiveIntegerField()
    content_object =  generic.GenericForeignKey('param_type', 'param_id')
    properties =   generic.GenericRelation(Property)
    required =        models.BooleanField(_('Required'), help_text=_('Is the parameter required?'))
    
    #the object this parameter is associated with
    content_type = models.ForeignKey(ContentType, 
                                     blank=True, null=True, 
                                     related_name='to_function',
                                     limit_choices_to=Q(jsobjects|jsfunction|jsclass))
    object_id =       models.PositiveIntegerField(blank=True, null=True)    
    function_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return self.name
class Function(StandardDocumentModel):
    ''' 
        Functions should be attached to any JavaScriptObject or any thing'
        that subclasses a JavaScript Object ( Class, NameSpace)
        
        Functions do not need to be attached to another object. In this
        case they would be considered global functions
    '''
    example_code =   models.TextField()
    availablity =    models.ForeignKey(JaxerRelease, blank=True, null=False,
                                       related_name="available_in")
    
    is_depricated =  models.BooleanField()
    depricated =     models.ForeignKey(JaxerRelease,blank=True, null=True,
                                        related_name="deripacted_in")

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
    return_param =  models.CharField(_('Variable Name'), max_length=50, 
                                     blank=True, null=True)
    return_type =   models.ForeignKey(ContentType, blank=True, 
                                      null=True, related_name='returntype')
    
    type_id =       models.PositiveIntegerField(_("Object's ID"), blank=True, null=True)
    return_object = generic.GenericForeignKey('return_type','type_id') 
    
    # parameters which make up the function signature
    parameters =    generic.GenericRelation(Parameter)
    admin_objects = GlobalFunctionManager()
    objects =       Manager()
    def __unicode__(self):
        return '%s' % self.name

    def get_return_type(self):
        if self.return_type is None:
            return 'void'
        else:
            return '%s' % self.return_type
    class Meta:
        verbose_name = "Function"   
        
# to be sub classed
class JavascriptObject(StandardDocumentModel):
    '''
        Representation of the JavaScript Object
        Naitive objects would be Array, String
    '''

    naitive =          models.BooleanField(help_text=_('Is this a naitive JS Object?'))
    properties =       generic.GenericRelation(Property)
    methods =          generic.GenericRelation(Function)     
    admin_objects =    NaitiveObjectManager()
    objects =          Manager()
    
    class Meta:
        verbose_name = 'Object'
    def __unicode__(self):
        return self.name
    def type(self):
        return "Object"
    
class JaxerNameSpace(JavascriptObject):
    #this is a subclass used to organize Jaxer's Namespace Objects
    #apart from the Standard javascript Objects(String, Array, etc)
    parent_namespace = models.ForeignKey('self', blank=True, null=True)
    objects =          CustomObjectManager()
    
    class Meta:
        verbose_name = "Namespace"
        
    def __unicode__(self):
        return self.name

        
class ClassItem(Function):
    
    '''
       ClassItem reprsents class which resideds inside of a namespace
       the name classitem was used to prevent naming conflicts
       
       Javascript does not have classes, they are actually functions
       Treated as objects - 
    '''
    namespace = models.ForeignKey(JaxerNameSpace)
    methods =     generic.GenericRelation(Function, 
                                          related_name='classmethods')  
       
    properties =  generic.GenericRelation(Property, 
                                          related_name='classproperites')

    def __unicode__(self):
        return ".".join([self.namespace.parent_namespace.name,self.namespace.name, self.name])   
    def class_name(self):
        return self.__unicode__()
    def type(self):
        return "%s Instance" % self.__unicode__()
    def save(self, force_insert=False, force_update=False):
        self.make_indexable()
        super(ClassItem, self).save(force_insert, force_update)
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        