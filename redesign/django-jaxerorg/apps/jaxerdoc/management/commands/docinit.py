from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from jaxerdoc.models import JavascriptObject
from jaxerdoc.management.commands import get_response

class Command(BaseCommand):
    help = ('Creates the initial Naitive Javascript objects for use in the JaxerDocs app\nThis will not create the methods or properties on the objects\nonly the objects themselves')
    requires_model_validation = True
    can_import_settings = True
    def handle(self, *args, **kwargs):
        return init(*args, **kwargs)

def init(*args, **kwargs):
    msg = "\nJaxerdoc needs to set up the naitive javascript objects\nfor use in the application.\n\nWould you like to do this now? (yes, no)"
    try:
        u = User.objects.filter(is_superuser = True)[0]
    except:
        print "Please Run the syncdb management command and create a Superuser"
        return
    jso = JavascriptObject.objects.filter(naitive=True)
    if get_response(msg, lambda inp:inp == 'yes', False):
        try:
            jso.get(name = 'Object')
        except:
            obj =  JavascriptObject(editor=u, 
                                    name='Object', 
                                    content='The Javascript Object Literal. A Hashmap of key/value pairs, where a value can be any other object', 
                                    naitive=True)
            obj.save()
        try:
            jso.get(name = 'String')
        except:
        
            str =  JavascriptObject(editor=u,
                                   name='String',
                                   content='The JavaScript object used to deal with text',
                                   naitive=True)
            str.save()
        try:
            jso.get(name = 'Number')
        except:
            num =  JavascriptObject(editor=u,
                                    name='Number',
                                    content='The javascript object used as a wrapper for basice numeric values',
                                    naitive=True)
            num.save()
        try:
            jso.get(name = 'Array')
        except:        
            arr =  JavascriptObject(editor=u,
                                    name='Array',
                                    content='',
                                    naitive=True)
            arr.save()
        try:
            jso.get(name = 'Boolean')
        except:        
            bool = JavascriptObject(editor=u,
                                    name='Boolean',
                                    content='The Javascript object used for dealing with true/false cases',
                                    naitive=True)
            bool.save()
        try:
            jso.get(name = 'Function')
        except:                
            func = JavascriptObject(editor=u,
                                    name='Function',
                                    content='The executable JavaScript Object',
                                    naitive=True)
            func.save()
        try:
            jso.get(name = 'Date')
        except:
            date = JavascriptObject(editor=u,
                                    name='Date',
                                    content='The JavaScript object used for dealing with dates and time',
                                    naitive=True)
            date.save()
        try:
            jso.get(name = 'Math')
        except:
            math = JavascriptObject(editor=u,
                                    name='Math',
                                    content='The JavaScript object which contains functionality for complex mathematical operations',
                                    naitive=True)
            math.save()
        try:
            jso.get(name = 'RegEx')
        except:
            math = JavascriptObject(editor=u,
                                    name='RegEx',
                                    content='The JavaScript ojbect for dealing with Regular Expressions - patterns of characters with in text',
                                    naitive=True)
            math.save()            
        print 'Success!'
    msg = '\nJaxerdoc benefits greatly from a Moderators Group.\nWould you like to create that group now? (yes, no)'
    if get_response(msg, lambda inp:inp == 'yes', False):    
        from django.contrib.auth.models import Group, Permission
        try:
            g = Group.objects.get(name='Documentation Moderators')
            print '\nIt looks like that group already exists!'
        except:
            g = Group(name="Documentation Moderators")
            g.save()
            perm = Permission.objects.get(codename='can_moderate_docs')
            g.permissions.add(perm)
            g.save()
            print "\nThe group %s has been created" % g.name
        