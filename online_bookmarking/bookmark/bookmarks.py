#todos -- append the uid of the user
#change the name of the template
#get bookmarks
#update page after adding bookmarks
#blocked coz of auth module
#if public add bookmarks to followers
#once signed in should be redirected to corresponding page

from django.shortcuts import render_to_response
from django.http import  Http404,HttpResponseRedirect,HttpResponse
from django.template import RequestContext

import json
import datetime

from bookmark.forms import BookmarkForm
from redis_helpers.views import Redis
from auth.login_status import is_logged_in
from auth.signin import login

def get_next_bookmarkId(redis_obj):
	''' Get the next unique bookmark id '''

	key = "global:bookmarkId"
	return Redis.next_unique_key(redis_obj,key)

def store_url(redis_obj,bookmark_id,url):
	''' Store the url of the bookmark '''  

	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.set_value(key,url)

def store_name(redis_obj,bookmark_id,name):
	''' store the name of the bookmark '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.set_value(key,name)

def store_description(redis_obj,bookmark_id,description):
	''' store the description of the bookmark '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.set_value(key,description)

def store_visibility(redis_obj,bookmark_id,visibility):
	''' store the visibility of bookmark '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.set_value(key,visibility)

def store_created_date(redis_obj,bookmark_id,created_date):
	''' store the creation time of bookmark '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.set_value(key,created_date)

def store_userId(redis_obj,bookmark_id,user_id):
	''' store the user id in the bookmark '''

	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.set_value(key,user_id)

def store_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	''' store the user's bookmarks in a list (stack implementation) '''

	key = "userId:%d:bookmarks" % (int(user_id))
	redis_obj.add_to_stack(key,bookmark_id)

def get_bookmark_uid_mapping_all(redis_obj, user_id):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_value(key)

def get_bookmark_uid_mapping_range(redis_obj, user_id, start, end):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_elements_in_range(key, start, end)

def get_name(redis_obj, bookmark_id):
	''' Retrieve bookmark name '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	return redis_obj.get_value(key)

def get_created_date(redis_obj, bookmark_id):
	''' Retrieve bookmark creation time '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	return redis_obj.get_value(key)

def get_description(redis_obj, bookmark_id):
	''' Retrieve bookmark description '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	return redis_obj.get_value(key)

def get_url(redis_obj, bookmark_id):
	''' Retrieve bookmark URL '''

	key = "bookmarkId:%d:url" % (bookmark_id)
	return redis_obj.get_value(key)

def get_visibility(redis_obj, bookmark_id):
	''' Retrieve bookmark visibility '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	return redis_obj.get_value(key)

def store_bookmark(request,bookmark_form):
	''' A controller which calls the individual store methods '''

	redis_obj = Redis()
	bookmark_id = get_next_bookmarkId(redis_obj)
	store_url(redis_obj,bookmark_id,bookmark_form['url'])
	store_name(redis_obj,bookmark_id,bookmark_form['name'])
	store_description(redis_obj,bookmark_id,bookmark_form['description'])
	store_visibility(redis_obj,bookmark_id,bookmark_form['visibility'])
	store_created_date(redis_obj,bookmark_id,str(datetime.datetime.now()))
	store_userId(redis_obj,bookmark_id,get_userId(request))
	store_bookmark_uid_mapping(redis_obj,bookmark_id,get_userId(request))

def get_userId(request):
	''' Get the user id by extracting auth token from cookies which is passed in the request '''

	redis_obj = Redis()
	auth_token = request.COOKIES.get('auth','')

	key = "auth.token:%s:userId" %(auth_token)
	return redis_obj.get_value(key)

def create_bookmark(request):
	''' View function which handles rendering the bookmark form and 
	stores them if valid or re-renders '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")
	if not is_logged_in(email,auth_token):
		return login(request)


	if request.method == "POST":

		bookmark_form = BookmarkForm(data=request.POST)
		
		if bookmark_form.is_valid():
			bookmark_form = bookmark_form.cleaned_data
			store_bookmark(request,bookmark_form)
			return HttpResponseRedirect('/success/')

		return render_to_response('add.html',
			{'bookmark_form':bookmark_form},context_instance=RequestContext(request))

	bookmark_form = BookmarkForm()
	return render_to_response('add.html',
		{'bookmark_form':bookmark_form},context_instance=RequestContext(request))

def display_bookmarks(request):
	''' Display existing bookmarks '''

	redis_obj = Redis()
	uid = get_userId(request)
	bookmarks = get_bookmark_uid_mapping_range(redis_obj, uid, 0, 10)

	data = [{} for i in xrange(len(bookmarks))]

	for i, bookmark_id in enumerate(bookmarks):
		data_dic ={}
		bookmark_id = int(bookmark_id)
		data_dic['name'] = get_name(redis_obj, bookmark_id)
		data_dic['url'] = get_url(redis_obj, bookmark_id)
		data_dic['visibility'] = get_visibility(redis_obj, bookmark_id)
		data_dic['creation_date'] = get_created_date(redis_obj, bookmark_id)
		data_dic['description'] = get_description(redis_obj, bookmark_id)
	
		data[i] = data_dic
		

	return render_to_response('home.html', {'uid' : uid, 'bookmarks' : data})	