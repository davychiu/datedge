from django import forms

class QuestionForm(forms.Form):
    def __init__(self, options, initial=None, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer'] = forms.ChoiceField(choices=[ (idx, ['A','B','C','D','E'][idx] + '. ' + o) for idx, o in enumerate(options)], initial=initial, widget=forms.RadioSelect())
