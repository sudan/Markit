from django import forms

class BookmarkForm(forms.Form):
	url = forms.URLField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Enter a url'}))
	name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Enter a name'}))
	description = forms.CharField(widget=forms.widgets.Textarea(attrs={'placeholder':'Enter a description'}))
	visibility = forms.ChoiceField(required=True,widget=forms.widgets.RadioSelect(),choices=[['public','public'],['private','private']])