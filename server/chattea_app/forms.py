from django import forms

class SubmitMessage(forms.Form):
    message = forms.CharField(max_length=5000, required=True)
