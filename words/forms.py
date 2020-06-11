from django import forms

LANGUAGE_CHOICES= [
    ('pl', 'Polski'),
    ('en', 'English'),
    ]

class WordsForm(forms.Form):
    field = forms.CharField(
        max_length=300, widget=forms.Textarea(attrs={"placeholder": "learn\nnew\nwords\n..."})
    )
    language = forms.CharField(label='Origin language:', widget=forms.Select(choices=LANGUAGE_CHOICES))
