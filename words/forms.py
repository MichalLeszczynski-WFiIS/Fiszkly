from django import forms


class WordsForm(forms.Form):
    field = forms.CharField(
        max_length=300, widget=forms.Textarea(attrs={"placeholder": "learn\nnew\nwords\n..."})
    )
