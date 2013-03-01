from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from auth.forms import PasswordChangeForm
from auth.helpers import get_userId
from auth.encrypt import encrypt_password
from auth.getters import get_password
from auth.signup import store_password
from auth.login_status import is_logged_in
from auth.signin import login,authentication

from redis_helpers.views import Redis

from online_bookmarking.settings import CHANGE_PASSWORD_TEMPLATE_PATH

@authentication('/change_password')
def change_password(request):
	''' Module for changing the password of the user '''

	if request.method == "POST":
		
		password_change_form = PasswordChangeForm(data=request.POST)
		if password_change_form.is_valid():
			
			password_change_form_cleaned = password_change_form.cleaned_data
			old_password = encrypt_password(password_change_form_cleaned['old_password'])
			user_id = get_userId(request)
			redis_obj = Redis()
			
			if get_password(redis_obj,user_id) == old_password:
				store_password(redis_obj,user_id,encrypt_password(password_change_form_cleaned['new_password']))
				return HttpResponseRedirect('/success/')
			
			return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
				{
				'password_change_form':password_change_form,
				'error':'Password you gave is incorrect'
				},
				context_instance=RequestContext(request))
		
		return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
			{
				'password_change_form':password_change_form,
				'error':'Invalid password entries'
			},
			context_instance=RequestContext(request))
	
	password_change_form = PasswordChangeForm()
	return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
		{
			'password_change_form':password_change_form
		},
		context_instance=RequestContext(request))