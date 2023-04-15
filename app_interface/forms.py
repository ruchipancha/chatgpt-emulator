from django import forms

class IDInputForm(forms.Form):
    id_field = forms.CharField(max_length=100, required= True)

class StorySubmitForm(forms.Form):
    story = forms.CharField(widget=forms.Textarea(attrs={"cols":100,"rows":6}),required=True)


# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)