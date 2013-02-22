from django import forms

class TagForm(forms.Form):
	name = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Tag Name'}))

