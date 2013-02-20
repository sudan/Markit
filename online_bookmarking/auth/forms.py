from django import forms

class SignUpForm(forms.Form):
	email = forms.EmailField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Enter your email '}))
	username = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'username'}))
	first_name = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'First name'}))
	last_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Last name'}))
	password = forms.CharField(required=True,widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))
	password_confirmation = forms.CharField(required=True,widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password Confirmation'}))
	
class LoginForm(forms.Form):
	email = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Enter your email'}))
	password = forms.CharField(required=True,widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))