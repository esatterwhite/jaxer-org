from django import forms
from jaxertagging.forms.fields import CommaSeperatedObjectField
class TestForm(forms.Form):
    objects = CommaSeperatedObjectField(label="related", help_text="a list of related objects")
    
    def save(self):
        import pdb
        pdb.set_trace()
        data = self.cleaned_data
        print data
        return data['objects']