from django import forms

class BookmarkForm(forms.Form):
	url = forms.URLField(error_messages={'required':'Invalid url'},widget=forms.widgets.TextInput(attrs={'placeholder':'Enter a url'}))
	name = forms.CharField(required=False,widget=forms.widgets.TextInput(attrs={'placeholder':'Enter a name'}))
	description = forms.CharField(required=False,widget=forms.widgets.Textarea(attrs={'placeholder':'Enter a description'}))
	visibility = forms.ChoiceField(error_messages={'required':'Invalid visibility'},widget=forms.widgets.RadioSelect(),choices=[['public','public'],['private','private']])