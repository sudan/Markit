from django import forms

class TagForm(forms.Form):
	name = forms.CharField(error_messages={'required':'Invalid tag name'},widget=forms.widgets.TextInput(attrs={'placeholder':'Tag Name'}))

