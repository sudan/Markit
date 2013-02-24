#todos timestamp required??
#after signup login again
#custom error messages for forms in auth and bookmarks

from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import hashlib
import md5
import datetime

from auth.forms import SignUpForm
from auth.encrypt import encrypt_password
from auth.helpers import get_auth_token,store_auth_token
from redis_helpers.views import Redis

def get_next_userId(redis_obj):
	''' Get the next unique user id '''
	
	key = "global:userId"
	return Redis.next_unique_key(redis_obj,key)

def store_global_userIds(redis_obj,user_id):
	''' Store the list of user ids '''

	key = "global:users:userId"
	redis_obj.add_to_set(key,user_id)

def store_email(redis_obj,user_id,email):
	''' store the email id of the user '''
	
	key = "userId:%d:email" % (user_id)
	redis_obj.set_value(key,email)

def store_username(redis_obj,user_id,username):
	''' store the username of the user '''
	
	key = "userId:%d:username" % (user_id)
	redis_obj.set_value(key,username)

def store_first_name(redis_obj,user_id,first_name):
	''' store the first name of the user '''
	
	key = "userId:%d:first.name" % (user_id)
	redis_obj.set_value(key,first_name)

def store_last_name(redis_obj,user_id,last_name):
	''' store the last name of the user '''
	
	key = "userId:%d:last.name" % (user_id)
	redis_obj.set_value(key,last_name)

def store_password(redis_obj,user_id,password):
	''' store the password of the user '''
	
	key = "userId:%d:password" % (user_id)
	redis_obj.set_value(key,password)

def store_image_url(redis_obj,user_id,email):
	''' store the gravatar  image url of the user '''
	
	key = "userId:%d:image" %(user_id)
	image_url = "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(email).hexdigest()
	redis_obj.set_value(key,image_url)

def store_timestamp(redis_obj,user_id):
	''' store the timestamp of the user creation '''
	
	key = "userId:%d:timestamp" %(user_id)
	redis_obj.set_value(key,str(datetime.datetime.now()))

def store_uid_with_username(redis_obj,user_id,username):
	''' store the reverse mapping for the username '''
	
	key = "username:%s:userId" % (username)
	redis_obj.set_value(key,user_id)

def store_uid_with_email(redis_obj,user_id,email):
	''' store the reverse mapping for the email id '''
	
	key = "email:%s:userId" % (email)
	redis_obj.set_value(key,user_id)

def store_uid_with_auth_token(redis_obj,user_id,auth_token):
	''' store the reverse mapping for auth token '''
	
	key = "auth.token:%s:userId" % (auth_token)
	redis_obj.set_value(key,user_id)

def store_email_with_auth_token(redis_obj,email,auth_token):
	''' store the reverse mapping for auth token '''
	
	key = "auth.token:%s:email" % (auth_token)
	redis_obj.set_value(key,email)

def store_user_info(signup_form):
	''' A controller which calls the individual store methods '''
	
	redis_obj = Redis()

	username = signup_form['username']
	email = signup_form['email']
	first_name = signup_form['first_name']
	last_name = signup_form['last_name']
	password = encrypt_password(signup_form['password'])
	auth_token = signup_form['auth_token']

	user_id = get_next_userId(redis_obj)

	store_email(redis_obj,user_id,email)
	store_username(redis_obj,user_id,username)
	store_first_name(redis_obj,user_id,first_name)
	store_last_name(redis_obj,user_id,last_name)
	store_password(redis_obj,user_id,password)
	store_image_url(redis_obj,user_id,email)
	store_timestamp(redis_obj,user_id)
	store_auth_token(redis_obj,user_id,email,auth_token)
	store_uid_with_username(redis_obj,user_id,username)
	store_uid_with_email(redis_obj,user_id,email)
	store_uid_with_auth_token(redis_obj,user_id,auth_token)
	store_email_with_auth_token(redis_obj,email,auth_token)
	store_global_userIds(redis_obj,user_id)

def username_exists(username):
	'''  check for the existence of a username '''
	
	redis_obj = Redis()
	return redis_obj.check_existence("username:%s:userId" % (username))


def email_exists(email):
	'''  check for the existence of email '''
	
	redis_obj = Redis()
	return redis_obj.check_existence("email:%s:userId" % (email))
    
def register(request):
	''' signup functionality which returns a empty form when given a GET request or
	validates n creates an entry in db with POST request '''

	if request.method == "POST":
		
		signup_form = SignUpForm(data=request.POST)
		if signup_form.is_valid():
			
			signup_form_cleaned = signup_form.cleaned_data

			if  signup_form_cleaned['password'] != signup_form_cleaned['password_confirmation']:
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'password doesnt match'},context_instance=RequestContext(request))
			
			if username_exists(signup_form_cleaned['username']) == 1:
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'username already exists'},context_instance=RequestContext(request))
			
			if email_exists(signup_form_cleaned['email']) == 1:
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'email id has already taken'},context_instance=RequestContext(request))

			password = encrypt_password(signup_form_cleaned['password'])
			password_confirmation = encrypt_password(signup_form_cleaned['password_confirmation'])
			signup_form_cleaned['auth_token'] = get_auth_token()

			store_user_info(signup_form_cleaned)
			response = HttpResponseRedirect('/home')

			max_age = 7 * 24 * 60 * 60
			expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
			response.set_cookie('auth',signup_form_cleaned['auth_token'], max_age=max_age, expires=expires)
			response.set_cookie('email',signup_form_cleaned['email'], max_age=max_age, expires=expires)
			return response
		
		return render_to_response('signup.html',{'signup_form':signup_form},context_instance=RequestContext(request))

	signup_form = SignUpForm()
	return render_to_response('signup.html',{'signup_form':signup_form},context_instance=RequestContext(request))



    
    
    
