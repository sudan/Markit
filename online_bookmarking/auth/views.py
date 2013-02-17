from django.shortcuts import render_to_response

def login(request):
    ''' Login form '''
    return render_to_response('login.html')

def home(request):
    ''' Home page '''
    return render_to_response('home.html')
