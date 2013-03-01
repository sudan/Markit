from django.http import Http404,HttpResponseRedirect
from django.template import RequestContext

from redis_helpers.views import Redis
from auth.helpers import get_auth_token,get_userId,store_auth_token
from auth.setters import *

def logout(request):
	''' Logout functionality '''
	
	auth_token = request.COOKIES.get("auth",None)
	email = request.COOKIES.get("email",None)

	try:
		if auth_token != None and email != None:
			
			redis_obj = Redis()
			old_auth_token = redis_obj.get_value("email:%s:auth.token" %(email))
			new_auth_token = get_auth_token()

			key = "email:%s:auth.token" % (email)
			redis_obj.set_value(key,new_auth_token)

			key = "auth.token:%s:email" % (new_auth_token)
			redis_obj.set_value(key,email)

			redis_obj.remove_key("auth.token:%s:email" % (old_auth_token))

			user_id = get_userId(request)
		
			key = "auth.token:%s:userId" %(new_auth_token)
			redis_obj.set_value(key,user_id)

			redis_obj.remove_key("auth.token:%s:userId" %(old_auth_token))

			key = "userId:%d:auth.token" %(user_id)
			redis_obj.set_value(key,new_auth_token)
	except:
		pass


	return HttpResponseRedirect('/')