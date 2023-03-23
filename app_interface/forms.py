from django import forms

class IDInputForm(forms.Form):
    id_field = forms.CharField(max_length=100, required= True)
