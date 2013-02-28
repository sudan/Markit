from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def login(request):
    ''' Login form '''
    return render_to_response('login.html')

def index(request):
	''' Home page '''

	return render_to_response('base.html',
		context_instance=RequestContext(request))

