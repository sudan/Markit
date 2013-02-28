from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from auth.forms import LoginForm
from redis_helpers.views import Redis
from auth.encrypt import encrypt_password
from auth.helpers import get_auth_token,store_auth_token
from auth.login_status import is_logged_in

import datetime

def  account_existence(redis_obj,email):
	''' Check for the existence of an account '''
	
	key = "email:%s:userId" % (email)
	return redis_obj.check_existence(key)

def get_key(redis_obj,email):
	''' Get the key using email '''
	
	key = "email:%s:userId" % (email)
	return int(redis_obj.get_value(key))

def get_password(redis_obj,user_id):
	''' Get the encrypted password using userid '''

	key = "userId:%d:password" % (user_id)
	return redis_obj.get_value(key)

def update_auth_token(redis_obj,auth_token,user_id,email):	
	''' Get the old auth token and update it accordingly '''
	
	key = "userId:%d:auth.token" % (user_id)
	old_auth_token = redis_obj.get_value(key)
	redis_obj.remove_key("auth.token:%s:userId" % (old_auth_token))
	
	store_auth_token(redis_obj,user_id,email,auth_token)

	key = "auth.token:%s:userId" % (auth_token)
	redis_obj.set_value(key,user_id)

	key = "auth.token:%s:email" % (auth_token)
	redis_obj.set_value(key,email)

def authentication(redirect_uri):
	''' A decorator for authentication '''

	def authentication_wrapper(func):
		
		def wrapper_func(request,*args,**kwargs):
			
			email = request.COOKIES.get("email","")
			auth_token = request.COOKIES.get("auth","")

			if not is_logged_in(email,auth_token):
				return login(request,redirect_uri)

			return func(request,*args,**kwargs)
		
		return wrapper_func
	
	return authentication_wrapper

def login(request,redirect_uri='/home'):
	''' login functionality which returns a empty form when given a GET request 
	or validates the authentication when given a POST request '''

	if request.method == "POST":
		login_form = LoginForm(data=request.POST)
		
		if login_form.is_valid():
			login_form_cleaned = login_form.cleaned_data
			email = login_form_cleaned['email']
			redis_obj = Redis()
			
			if account_existence(redis_obj,email) == 1:
				user_id = get_key(redis_obj,email)
				password = get_password(redis_obj,user_id)
				
				if password == encrypt_password(login_form_cleaned['password']):
					auth_token = get_auth_token()
					
					update_auth_token(redis_obj,auth_token,user_id,email)
					redirect_uri =  request.POST.get('redirect_uri','/home')
					response = HttpResponseRedirect(redirect_uri)
					max_age = 7 * 24 * 60 * 60
					expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
					response.set_cookie('auth',auth_token,max_age=max_age, expires=expires)
					response.set_cookie('email',email,max_age=max_age, expires=expires)
					return response
		
		redirect_uri =  request.POST.get('redirect_uri','/home')
		return render_to_response('auth/login.html',{'login_form':login_form,'redirect_uri':redirect_uri,'error':'invalid username or password'},context_instance=RequestContext(request))
	
	login_form = LoginForm()
	return render_to_response('auth/login.html',{'login_form':login_form,'redirect_uri':redirect_uri,},context_instance=RequestContext(request))
				






