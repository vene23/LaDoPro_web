from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=120)
    email = forms.EmailField()
    asunto = forms.CharField(max_length=200, required=False)
    mensaje = forms.CharField(widget=forms.Textarea)
