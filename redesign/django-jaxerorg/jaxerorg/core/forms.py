''' jaxerorg forms.py '''
from django import forms
from django.template.defaultfilters import force_escape
from django.utils.html import escape

class InsertCodeForm(forms.Form):
    '''    
        this is an unbound form for the site WYSIWYG editor. The submission of
        this form is handled completely via javascript by the client.
    '''
    _help = escape('omit javascript start / end tags (<script>, <?php, etc)')
    LANGUAGES = (
    #@attention: this is used to determine the syntax highlighting
    #            currently, these are the only options that are completed
    #            if you decide to add a new one, you will need to add the
    #            corresponding javascript and CSS files to match 
        ('js', 'JavaScript'),
        ('html', 'HTML'),
        ('css','CSS'),
        ('php','PHP'),
        ('ruby','Ruby'),
        ('sql','SQL'),
        ('md','MarkDown'),
        ('shell','Shell')
    )
    
    language = forms.ChoiceField(choices=LANGUAGES)
    code =     forms.CharField(
                                    help_text=_help,
                                    widget=forms.Textarea(attrs={'cols':40})
                              )
