from django import template
from jaxerlog.models import UserLogEntry
from django.contrib.contenttypes.models import ContentType
register = template.Library()

class UserLogNode(template.Node):
    def __init__(self, limit, varname, user):
        self.limit, self.varname, self.user = limit, varname, user

    def __repr__(self):
        return "<UserLog Node>"

    def render(self, context):
        import pdb
        pdb.set_trace()
        if self.user is None:
            context[self.varname] = UserLogEntry.objects.all().select_related('content_type', 'user')[:self.limit]
        else:
            user_id = self.user
            if not user_id.isdigit():
                user_id = context[self.user].id
            context[self.varname] = UserLogEntry.objects.filter(member__id__exact=user_id).select_related('content_type', 'user')[:self.limit]
        return ''

class DoGetUserLog:
    """
    Populates a template variable with the admin log for the given criteria.

    Usage::

        {% get_user_log [limit] as [varname] for_user [context_var_containing_user_obj] %}

    Examples::

        {% get_user_log 10 as user_log for_user 23 %}
        {% get_user_log 10 as user_log for_user user %}
        {% get_user_log 10 as user_log %}

    Note that ``context_var_containing_user_obj`` can be a hard-coded integer
    (user ID) or the name of a template context variable containing the user
    object whose ID you want.
    """
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        import pdb
        pdb.set_trace()
        tokens = token.contents.split()
        if len(tokens) < 4:
            raise template.TemplateSyntaxError, "'%s' statements require two arguments" % self.tag_name
        if not tokens[1].isdigit():
            raise template.TemplateSyntaxError, "First argument in '%s' must be an integer" % self.tag_name
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument in '%s' must be 'as'" % self.tag_name
        if len(tokens) > 4:
            if tokens[4] != 'for_user':
                raise template.TemplateSyntaxError, "Fourth argument in '%s' must be 'for_user'" % self.tag_name
        return UserLogNode(limit=tokens[1], varname=tokens[3], user=(len(tokens) > 5 and tokens[5] or None))


class ObjectLogNode(template.Node):
    def __init__(self, limit, varname, obj):
        self.limit, self.varname, self.obj = limit, varname, obj

    def __repr__(self):
        return "<ObjectLog Node>"

    def render(self, context):
        if self.user is None:
            context[self.varname] = UserLogEntry.objects.all().select_related('content_type', 'user')[:self.limit]
        else:
            ct = ContentType.objects.get_for_model(self.obj)
            obj_id = context[self.obj].id
            context[self.varname] = UserLogEntry.objects.filter(content_type = ct, object_id = obj_id).select_related('content_type', 'user')[:self.limit]
        return ''

class DoGetObjectLog:
    """
    Populates a template variable with the admin log for the given criteria.

    Usage::

        {% get_user_log [limit] as [varname] for_user [context_var_containing_user_obj] %}

    Examples::

        {% get_user_log 10 as user_log for_user user %}
        {% get_user_log 10 as user_log %}

    Note that ``context_var_containing_user_obj`` can be a hard-coded integer
    (user ID) or the name of a template context variable containing the user
    object whose ID you want.
    """
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __call__(self, parser, token):
        tokens = token.contents.split()
        if len(tokens) < 4:
            raise template.TemplateSyntaxError, "'%s' statements require two arguments" % self.tag_name
        if not tokens[1].isdigit():
            raise template.TemplateSyntaxError, "First argument in '%s' must be an integer" % self.tag_name
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "Second argument in '%s' must be 'as'" % self.tag_name
        if len(tokens) > 4:
            if tokens[4] != 'for_object':
                raise template.TemplateSyntaxError, "Fourth argument in '%s' must be 'for_user'" % self.tag_name
        return UserLogNode(limit=tokens[1], varname=tokens[3], obj=(len(tokens) > 5 and tokens[5] or None))



register.tag('get_user_log', DoGetUserLog('get_user_log'))
register.tag('get_object_log', DoGetObjectLog('get_object_log'))