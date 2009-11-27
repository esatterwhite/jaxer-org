from django import forms

class AjaxObjectSearchbar(forms.TextInput):
    def __init__(self, attrs={}):
        return super(AjaxObjectSearchbar, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        renderd = super(AjaxObjectSearchbar, self).render(name, value, attrs)
        return renderd + ('''<script type='text/javascript'>
                               var JAXERAUTO = new AutoCompleter.Request.Json("id_%s", /search/objects/,{
                                'minLength': 1, // We need at least 1 character
                                'selectMode': 'type-ahead', // Instant completion
                                'postVar': 'searchVal',
                                'tokens': null,
                                'filterSubset':true,
                                'injectChoice':function(token){
                                    new Element('li',{
                                        'html':token.name
                                    }).inject(choice);
                                }
                                this.addChoiceEvents(choice).inject(this.choices)                           
                               });
                          </script>''')% name