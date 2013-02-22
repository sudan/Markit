from django import forms

class CategoryForm(forms.Form):
	name = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'category name'}))

	