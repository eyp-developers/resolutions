from django import forms

class ClausePositionForm(forms.Form):
    clause = forms.IntegerField(required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.IntegerField(required=True, widget=forms.Select(attrs={'class': 'form-control'}))

class SubtopicPositionForm(forms.Form):
    subtopic = forms.IntegerField(required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.IntegerField(required=True, widget=forms.Select(attrs={'class': 'form-control'}))

