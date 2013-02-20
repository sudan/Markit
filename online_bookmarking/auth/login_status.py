from django.http import Http404,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from redis_helpers.views import Redis
from auth.helpers import get_auth_token

def is_logged_in(cookie_email,cookie_auth_token):

	if cookie_auth_token == "" or cookie_email == "":
		return False

	redis_obj = Redis()
	auth_token = redis_obj.get_value("email:%s:auth.token" % (cookie_email))

	if auth_token != cookie_auth_token:
		return False

	email = redis_obj.get_value("auth.token:%s:email" % (cookie_auth_token))
	if email != cookie_email:
		return False

	return True