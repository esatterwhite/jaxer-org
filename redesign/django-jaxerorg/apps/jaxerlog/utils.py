from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect

def log_addition(request, obj, message ):
    """
    Log that an object has been successfully added. 
    
    The default implementation creates an MemberLogEntry object.
    """
    from jaxerlog.models import MemberLogEntry, LOG_ADDITION 
    MemberLogEntry.objects.log_action(
        user_id         = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        action_flag     = LOG_ADDITION,
        change_message = message
    )
    
def log_change(request, obj, message):
    """
    Log that an object has been successfully changed. 
    
    The default implementation creates an MemberLogEntry object.
    """
    from jaxerlog.models import MemberLogEntry, LOG_CHANGE
    MemberLogEntry.objects.log_action(
        user_id         = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(obj).pk, 
        object_id       = obj.pk, 
        action_flag     = LOG_CHANGE, 
        change_message  = message
    )
    
def log_deletion( request, obj, message):
    """
    Log that an object has been successfully deleted. Note that since the
    object is deleted, it might no longer be safe to call *any* methods
    on the object, hence this method getting object_repr.
    
    The default implementation creates an aMemberLogEntry object.
    """
    from jaxerlog.models import MemberLogEntry, LOG_DELETION
    MemberLogEntry.objects.log_action(
        user_id          = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(obj).pk, 
        object_id       = obj.pk, 
        action_flag     = LOG_DELETION,
        change_message =  message
    )
    

    
def redirect(obj, post_save_redirect=None):
    """
    Returns a HttpResponseRedirect to ``post_save_redirect``.

    ``post_save_redirect`` should be a string, and can contain named string-
    substitution place holders of ``obj`` field names.

    If ``post_save_redirect`` is None, then redirect to ``obj``'s URL returned
    by ``get_absolute_url()``.  If ``obj`` has no ``get_absolute_url`` method,
    then raise ImproperlyConfigured.

    This function is meant to handle the post_save_redirect parameter to the
    ``create_object`` and ``update_object`` views.
    """
    if post_save_redirect:
        try:
            return HttpResponseRedirect(post_save_redirect % obj.__dict__)
        except:
            return HttpResponseRedirect('/')
    elif hasattr(obj, 'get_absolute_url'):
        return HttpResponseRedirect(obj.get_absolute_url())
    else:
        raise ImproperlyConfigured(
            "No URL to redirect to.  Either pass a post_save_redirect"
            " parameter to the generic view or define a get_absolute_url"
            " method on the Model.")
        
def remove_logs_for_object(obj):
    from jaxerlog.models import MemberLogEntry
    object_type_id = ContentType.objects.get_for_model(obj).pk
    logs = MemberLogEntry.objects.filter(content_type__pk = object_type_id).filter(object_id = obj.pk)
    logs.delete()
