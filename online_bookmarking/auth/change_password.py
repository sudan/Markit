from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from auth.forms import ChangePasswordForm
from auth.helpers import get_userId
from auth.encrypt import encrypt_password
from auth.getters import get_password,get_username
from auth.signup import store_password
from auth.login_status import is_logged_in
from auth.signin import login, authentication

from redis_helpers.views import Redis

from online_bookmarking.settings import CHANGE_PASSWORD_TEMPLATE_PATH

@authentication('/change_password')
def change_password(request):
	''' Module for changing the password of the user '''

	redis_obj = Redis()
	user_id = get_userId(request)
	username = get_username(redis_obj,user_id)

	if request.method == "POST":
		
		change_password_form = ChangePasswordForm(data=request.POST)
		if change_password_form.is_valid():
			
			change_password_form_cleaned = change_password_form.cleaned_data
			old_password = encrypt_password(change_password_form_cleaned['old_password'])
			new_password = encrypt_password(change_password_form_cleaned['new_password'])
			
			if get_password(redis_obj, user_id) == old_password:
				store_password(redis_obj, user_id, new_password)
				return HttpResponseRedirect('/home')
			
			return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
				{
					'change_password_form':change_password_form,
					'change_password_error':'Password you gave is incorrect',
					'username':username
				},
				context_instance=RequestContext(request))
		
		return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
			{
				'change_password_form':change_password_form,
				'change_password_error':'Invalid password entries',
				'username':username
			},
			context_instance=RequestContext(request))
	
	change_password_form = ChangePasswordForm()
	return render_to_response(CHANGE_PASSWORD_TEMPLATE_PATH,
		{
			'change_password_form':change_password_form,
			'username':username,
		},
		context_instance=RequestContext(request))