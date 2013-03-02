from django import forms

class CategoryForm(forms.Form):
	name = forms.CharField(error_messages={'required':'Invalid category name'}, widget=forms.widgets.TextInput(attrs={'placeholder':'category name'}))

	