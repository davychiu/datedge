from django import forms

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        if options:
            self.fields['answer'] = forms.ChoiceField(choices=[ (idx, ['A','B','C','D','E'][idx] + '. ' + o) for idx, o in enumerate(options)], widget=forms.RadioSelect())
