from django.shortcuts import render_to_response, redirect

def login(request):
    ''' Login form '''
    return render_to_response('login.html')

