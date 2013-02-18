#todos timestamp required??
#after signup login again
#custom error messages for forms in auth and bookmarks

from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import hashlib
import random
import md5
import datetime

from auth.forms import SignUpForm
from auth.encrypt import encrypt_password
from auth.helpers import get_auth_token,store_auth_token
from redis_helpers.views import Redis

    
#Get the next unique user id
def get_next_userId(redis_obj):
	key = "global:userId"
	return Redis.next_unique_key(redis_obj,key)

#store the email id of the user 
def store_email(redis_obj,user_id,email):
	key = "userId:%d:email" % (user_id)
	redis_obj.set_value(key,email)

#store the username of the user
def store_username(redis_obj,user_id,username):
	key = "userId:%d:username" % (user_id)
	redis_obj.set_value(key,username)

#store the first name of the user
def store_first_name(redis_obj,user_id,first_name):
	key = "userId:%d:first.name" % (user_id)
	redis_obj.set_value(key,first_name)

#store the last name of the user
def store_last_name(redis_obj,user_id,last_name):
	key = "userId:%d:last.name" % (user_id)
	redis_obj.set_value(key,last_name)

#store the password of the user
def store_password(redis_obj,user_id,password):
	key = "userId:%d:password" % (user_id)
	redis_obj.set_value(key,password)

#store the gravatar  image url of the user
def store_image_url(redis_obj,user_id,email):
	key = "userId:%d:image" %(user_id)
	image_url = "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(email).hexdigest()
	redis_obj.set_value(key,image_url)

def store_timestamp(redis_obj,user_id):
	key = "userId:%d:timestamp" %(user_id)
	redis_obj.set_value(key,str(datetime.datetime.now()))

#store the reverse mapping for the username
def store_uid_with_username(redis_obj,user_id,username):
	key = "username:%s:userId" % (username)
	redis_obj.set_value(key,user_id)

#store the reverse mapping for the email id
def store_uid_with_email(redis_obj,user_id,email):
	key = "email:%s:userId" % (email)
	redis_obj.set_value(key,user_id)

#store the reverse mapping for auth token
def store_uid_with_auth_token(redis_obj,user_id,auth_token):
	key = "auth.token:%s:userId" % (auth_token)
	redis_obj.set_value(key,user_id)

#A controller which calls the individual store methods
def store_user_info(signup_form):
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
	store_auth_token(redis_obj,user_id,auth_token)
	store_uid_with_username(redis_obj,user_id,username)
	store_uid_with_email(redis_obj,user_id,email)
	store_uid_with_auth_token(redis_obj,user_id,auth_token)

# check for the existence of a username
def username_exists(username):
	redis_obj = Redis()
	return redis_obj.check_existence("username:%s:userId" % (username))

# check for the existence of email
def email_exists(email):
	redis_obj = Redis()
	return redis_obj.check_existence("email:%s:userId" % (email))
    
# signup functionality which returns a empty form when given a GET request or validates n creates an entry in db with POST request
def register(request):

	if request.method == "POST":
		
		signup_form = SignUpForm(data=request.POST)
		if signup_form.is_valid():
			
			signup_form = signup_form.cleaned_data

			if  signup_form['password'] != signup_form['password_confirmation']:
				signup_form = SignUpForm(data=request.POST)
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'password doesnt match'},context_instance=RequestContext(request))
			
			if username_exists(signup_form['username']) == 1:
				signup_form = SignUpForm(data=request.POST)
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'username already exists'},context_instance=RequestContext(request))
			
			if email_exists(signup_form['email']) == 1:
				signup_form = SignUpForm(data=request.POST)
				return render_to_response('signup.html',{'signup_form':signup_form,'error':'email id has already taken'},context_instance=RequestContext(request))

			password = encrypt_password(signup_form['password'])
			password_confirmation = encrypt_password(signup_form['password_confirmation'])
			signup_form['auth_token'] = get_auth_token()

			store_user_info(signup_form)
			response = HttpResponseRedirect('/home')

			max_age = 7 * 24 * 60 * 60
			expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
			response.set_cookie('auth',signup_form['auth_token'], max_age=max_age, expires=expires)
			response.set_cookie('email',signup_form['email'], max_age=max_age, expires=expires)
			return response
		
		signup_form = SignUpForm()
		return render_to_response('signup.html',{'signup_form':signup_form},context_instance=RequestContext(request))

	signup_form = SignUpForm()
	return render_to_response('signup.html',{'signup_form':signup_form},context_instance=RequestContext(request))



    
    
    
