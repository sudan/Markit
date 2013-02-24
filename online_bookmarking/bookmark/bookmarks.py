#change the name of the template
#update page after adding bookmarks
#if public add bookmarks to followers

from django.shortcuts import render_to_response,redirect
from django.http import  Http404,HttpResponseRedirect,HttpResponse
from django.template import RequestContext

import json
import datetime

from bookmark.forms import BookmarkForm
from redis_helpers.views import Redis
from auth.login_status import is_logged_in
from auth.signin import login
from auth.helpers import get_userId
from bookmark.getters import *
from bookmark.setters import *
from bookmark.deleters import *

def store_bookmark(request,bookmark_form):
	''' A controller which calls the individual store methods '''

	redis_obj = Redis()

	#PUT and POST requests are handled in the same view
	if bookmark_form.get('bookmark_id','') != '':
		bookmark_id = bookmark_form['bookmark_id']
	else:
		bookmark_id = get_next_bookmarkId(redis_obj)
		store_created_date(redis_obj,bookmark_id,str(datetime.datetime.now()))

	store_url(redis_obj,bookmark_id,bookmark_form['url'])
	store_name(redis_obj,bookmark_id,bookmark_form['name'])
	store_description(redis_obj,bookmark_id,bookmark_form['description'])
	store_visibility(redis_obj,bookmark_id,bookmark_form['visibility'])
	
	store_userId(redis_obj,bookmark_id,get_userId(request))
	store_bookmark_uid_mapping(redis_obj,bookmark_id,get_userId(request))

def clear_bookmark(user_id,bookmark_id):
	''' Delete all mappings associated with bookmark id '''

	redis_obj = Redis()
	delete_url(redis_obj,bookmark_id)
	delete_name(redis_obj,bookmark_id)
	delete_description(redis_obj,bookmark_id)
	delete_visibility(redis_obj,bookmark_id)
	delete_created_date(redis_obj,bookmark_id)
	delete_userId(redis_obj,bookmark_id)
	delete_category(redis_obj,bookmark_id)
	delete_bookmark_uid_mapping(redis_obj,bookmark_id,user_id)

def get_bookmarks(request):

	redis_obj = Redis()
	uid = get_userId(request)

	bookmarks = get_bookmark_uid_mapping_range(redis_obj, uid, 0, 10)
	data = [{} for i in xrange(len(bookmarks))]
	
	for i, bookmark_id in enumerate(bookmarks):

		data_dic ={}
		bookmark_id = int(bookmark_id)
		data_dic['bookmark_id'] = bookmark_id
		data_dic['name'] = get_name(redis_obj, bookmark_id)
		data_dic['url'] = get_url(redis_obj, bookmark_id)
		data_dic['visibility'] = get_visibility(redis_obj, bookmark_id)
		data_dic['creation_date'] = get_created_date(redis_obj, bookmark_id)
		data_dic['description'] = get_description(redis_obj, bookmark_id)
		
		data[i] = data_dic

	return uid , data


def create_bookmark(request):
	''' View function which handles rendering the bookmark form and 
	stores them if valid or re-renders '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request,redirect_uri='/bookmark')

	if request.method == "POST":

		bookmark_form = BookmarkForm(data=request.POST)
		
		if bookmark_form.is_valid():
			bookmark_form_cleaned = bookmark_form.cleaned_data
			store_bookmark(request,bookmark_form_cleaned)
			return HttpResponseRedirect('/success/')

		return render_to_response('add.html',
			{'bookmark_form':bookmark_form},context_instance=RequestContext(request))

	
	bookmark_form = BookmarkForm()
	return render_to_response('add.html',
			{'bookmark_form':bookmark_form},context_instance=RequestContext(request))



def display_bookmarks(request):
	''' Display existing bookmarks '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request,redirect_uri='/home')

	uid , data = get_bookmarks(request)		

	return render_to_response('home.html', {'uid' : uid, 'bookmarks' : data})	

def delete_bookmark(request):
	''' Delete a bookmark '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")
	
	if not is_logged_in(email,auth_token):
		return login(request,redirect_uri='/home')

	bookmark_id = request.POST.get("bookmark_id","")
	user_id = get_userId(request)

	if bookmark_id != "":
		clear_bookmark(int(user_id),int(bookmark_id))