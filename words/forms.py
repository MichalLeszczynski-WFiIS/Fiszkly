from django import forms

class WordsForm(forms.Form):
    field = forms.CharField(max_length=300, widget=forms.Textarea(attrs={"placeholder": "Insert your words separated by a space"}))
    