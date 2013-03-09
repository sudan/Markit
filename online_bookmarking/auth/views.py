from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from auth.forms import SignUpForm, LoginForm
from online_bookmarking.settings import HOME_PAGE_TEMPLATE_PATH
from auth.signin import is_logged_in

def login(request):
    ''' Login form '''
    return render_to_response('login.html')


def index(request):
	''' Home page for the project '''

	email = request.COOKIES.get("email", "")
	auth_token = request.COOKIES.get("auth", "")

	if is_logged_in(email, auth_token):
		return HttpResponseRedirect('/home')

	signup_form = SignUpForm()
	login_form = LoginForm()

	return render_to_response(HOME_PAGE_TEMPLATE_PATH,
		{
			'signup_form':signup_form,
			'login_form':login_form
		},
		context_instance=RequestContext(request))

