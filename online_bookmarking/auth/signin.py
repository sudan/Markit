from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from auth.forms import LoginForm
from redis_helpers.views import Redis
from auth.encrypt import encrypt_password
from auth.helpers import get_auth_token,store_auth_token

# Check for the existence of an account
def  account_existence(redis_obj,email):
	
	key = "email:%s:userId" % (email)
	return redis_obj.check_existence(key)

# Get the key using email
def get_key(redis_obj,email):

	key = "email:%s:userId" % (email)
	return redis_obj.get_value(key)

# Get the encrypted password using userid
def get_password(redis_obj,userId):

	key = "userId:%d:password" % (int(userId))
	return redis_obj.get_value(key)

# login functionality which returns a empty form when given a GET request or validates the authentication when given a POST request
def login(request):

	if request.method == "POST":
		login_form = LoginForm(data=request.POST)
		
		if login_form.is_valid():
			login_form = login_form.cleaned_data
			email = login_form['email']
			redis_obj = Redis()

			if account_existence(redis_obj,email) == 1:
				userId = get_key(redis_obj,email)
				password = get_password(redis_obj,userId)
				
				if password == encrypt_password(login_form['password']):
					response = HttpResponseRedirect('/home')
					auth_token = get_auth_token()
					response.set_cookie('auth',auth_token)
					return response
		
		login_form = LoginForm()
		return render_to_response('login.html',{'login_form':login_form,'error':'invalid username or password'},context_instance=RequestContext(request))
	
	login_form = LoginForm()
	return render_to_response('login.html',{'login_form':login_form},context_instance=RequestContext(request))
				






