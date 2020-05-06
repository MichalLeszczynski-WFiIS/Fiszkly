from django import forms


class QuestionForm(forms.Form):
    CHOICES=[('t','true'), ('f', 'false')]
    is_correct = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)