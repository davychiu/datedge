from django import forms
from django.utils.safestring import mark_safe

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', None)
        active = kwargs.pop('active', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        if options:
            self.fields['answer'] = forms.ChoiceField(choices=[ (idx, mark_safe(['A','B','C','D','E'][idx] + '. ' + o.replace("&apos;","'").replace("&#39;","'"))) for idx, o in enumerate(options) if o], widget=forms.RadioSelect(), required=False)
            if not active:
                self.fields['answer'].widget.attrs['readonly'] = True
