from django import forms
import re

class SignUpForm(forms.Form):
	email = forms.EmailField(error_messages={'required':'Invalid Email'},widget=forms.widgets.TextInput(attrs={'placeholder':'Enter your email '}))
	username = forms.CharField(error_messages={'required':'Invalid Username'},widget=forms.widgets.TextInput(attrs={'placeholder':'username'}))
	first_name = forms.CharField(error_messages={'required':'Invalid First Name'},widget=forms.widgets.TextInput(attrs={'placeholder':'First name'}))
	last_name = forms.CharField(required=False,widget=forms.widgets.TextInput(attrs={'placeholder':'Last name'}))
	password = forms.CharField(error_messages={'required':'Invalid Password'},widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))
	password_confirmation = forms.CharField(error_messages={'required':'Invalid Password Confirmation'},required=True,widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password Confirmation'}))

	def clean_username(self):
		username = self.cleaned_data['username']
		valid = re.match('^[\w]+$',username) is not None
		if not valid:
			raise forms.ValidationError('Username should contain only alpha numeric characters')
		return username 

class LoginForm(forms.Form):
	email = forms.CharField(error_messages={'required':'Invalid Email'},widget=forms.widgets.TextInput(attrs={'placeholder':'Enter your email'}))
	password = forms.CharField(error_messages={'required':'Invalid Password'},widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))