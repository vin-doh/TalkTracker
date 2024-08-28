from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)
    text_input = forms.CharField(widget=forms.Textarea, required=False)
