from django.template import RequestContext
from django.shortcuts import render_to_response,HttpResponseRedirect

from redis_helpers.views import Redis

from auth.login_status import is_logged_in
from auth.helpers import get_userId
from auth.getters import *
from auth.setters import *
from auth.deleters import *
from auth.signin import login,authentication

from auth.forms import EditProfileForm

def update_profile(redis_obj,edit_profile_form,user_id,old_username):
	''' a controller for update user profile '''

	store_first_name(redis_obj,user_id,edit_profile_form['first_name'])
	store_last_name(redis_obj,user_id,edit_profile_form['last_name'])
	store_username(redis_obj,user_id,edit_profile_form['username'])

	delete_uid_with_username(redis_obj,old_username)

	store_uid_with_username(redis_obj,user_id,edit_profile_form['username'])

@authentication('/edit_profile')
def edit_profile(request):
	''' Edit a user's profile '''

	redis_obj = Redis()
	user_id = get_userId(request)

	if request.method == "POST":
			edit_profile_form = EditProfileForm(data=request.POST)
			if edit_profile_form.is_valid():
				edit_profile_form_cleaned = edit_profile_form.cleaned_data

				username = get_username(redis_obj,user_id)

				update_profile(redis_obj,edit_profile_form_cleaned,user_id,username)
				return HttpResponseRedirect('/success/')

			return render_to_response('auth/edit_profile.html',{'edit_profile_form':edit_profile_form},
				context_instance=RequestContext(request))

	username = get_username(redis_obj,user_id)
	first_name = get_first_name(redis_obj,user_id)
	last_name = get_last_name(redis_obj,user_id)

	edit_profile_form = EditProfileForm(initial={
		'username':username,'first_name':first_name,'last_name':last_name
	})
	
	return render_to_response('auth/edit_profile.html',{'edit_profile_form':edit_profile_form},
		context_instance=RequestContext(request))