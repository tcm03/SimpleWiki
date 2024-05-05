from django import forms

class NewPageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.read_only_title = kwargs.pop('read_only_title', False)
        super(NewPageForm, self).__init__(*args, **kwargs)
        if self.read_only_title:
            self.fields['title'].widget.attrs['readonly'] = True
            
    title = forms.CharField(label="Page title", max_length=100)
    content = forms.CharField(widget=forms.Textarea, label="Page content")