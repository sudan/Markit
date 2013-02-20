from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from auth.forms import LoginForm
from redis_helpers.views import Redis
from auth.encrypt import encrypt_password
from auth.helpers import get_auth_token,store_auth_token

import datetime

def  account_existence(redis_obj,email):
	''' Check for the existence of an account '''
	
	key = "email:%s:userId" % (email)
	return redis_obj.check_existence(key)

def get_key(redis_obj,email):
	''' Get the key using email '''
	
	key = "email:%s:userId" % (email)
	return redis_obj.get_value(key)

def get_password(redis_obj,user_id):
	''' Get the encrypted password using userid '''

	key = "userId:%d:password" % (int(user_id))
	return redis_obj.get_value(key)

def update_auth_token(redis_obj,auth_token,user_id,email):	
	''' Get the old auth token and update it accordingly '''
	
	key = "userId:%d:auth.token" % (int(user_id))
	old_auth_token = redis_obj.get_value(key)
	redis_obj.remove_key("auth.token:%s:userId" % (old_auth_token))
	
	store_auth_token(redis_obj,int(user_id),email,auth_token)

	key = "auth.token:%s:userId" % (auth_token)
	redis_obj.set_value(key,user_id)

	key = "auth.token:%s:email" % (auth_token)
	redis_obj.set_value(key,email)


def login(request):
	''' login functionality which returns a empty form when given a GET request 
	or validates the authentication when given a POST request '''

	if request.method == "POST":
		login_form = LoginForm(data=request.POST)
		
		if login_form.is_valid():
			login_form = login_form.cleaned_data
			email = login_form['email']
			redis_obj = Redis()

			if account_existence(redis_obj,email) == 1:
				user_id = get_key(redis_obj,email)
				password = get_password(redis_obj,user_id)
				
				if password == encrypt_password(login_form['password']):
					auth_token = get_auth_token()
					
					update_auth_token(redis_obj,auth_token,user_id,email)

					response = HttpResponseRedirect('/home')
					max_age = 7 * 24 * 60 * 60
					expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
					response.set_cookie('auth',auth_token,max_age=max_age, expires=expires)
					response.set_cookie('email',email,max_age=max_age, expires=expires)
					return response
		
		login_form = LoginForm()
		return render_to_response('login.html',{'login_form':login_form,'error':'invalid username or password'},context_instance=RequestContext(request))
	
	login_form = LoginForm()
	return render_to_response('login.html',{'login_form':login_form},context_instance=RequestContext(request))
				






