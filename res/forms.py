from django import forms


class ClausePositionForm(forms.Form):
    clause = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    position = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class SubtopicPositionForm(forms.Form):
    subtopic = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    position = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ClauseCreateForm(forms.Form):
    position = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    INTRODUCTORY = 'IC'
    OPERATIVE = 'OC'
    CLAUSE_TYPES = (
        (INTRODUCTORY, 'Introductory Clause'),
        (OPERATIVE, 'Operative Clause')
    )

    type = forms.ChoiceField(choices=CLAUSE_TYPES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, subtopic_choices, *args, **kwargs):
        super(ClauseCreateForm, self).__init__(*args, **kwargs)
        self.fields['subtopic'].choices = subtopic_choices

    subtopic = forms.ChoiceField(choices=(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))


class SubtopicCreateForm(forms.Form):
    subtopic_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ClauseEditForm(forms.Form):
    position = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    def __init__(self, subtopic_choices, *args, **kwargs):
        super(ClauseEditForm, self).__init__(*args, **kwargs)
        self.fields['subtopic'].choices = subtopic_choices

    subtopic = forms.ChoiceField(choices=(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))