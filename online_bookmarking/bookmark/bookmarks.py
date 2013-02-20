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

#Get the next unique bookmark id
def get_next_bookmarkId(redis_obj):
	key = "global:bookmarkId"
	return Redis.next_unique_key(redis_obj,key)

#store the url of the bookmark 
def store_url(redis_obj,bookmark_id,url):
	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.set_value(key,url)

#store the name of the bookmark
def store_name(redis_obj,bookmark_id,name):
	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.set_value(key,name)

#store the description of the bookmark
def store_description(redis_obj,bookmark_id,description):
	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.set_value(key,description)

#store the visibility of bookmark
def store_visibility(redis_obj,bookmark_id,visibility):
	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.set_value(key,visibility)

#store the creation time of bookmark
def store_created_date(redis_obj,bookmark_id,created_date):
	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.set_value(key,created_date)

#store the user id in the bookmark
def store_userId(redis_obj,bookmark_id,user_id):
	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.set_value(key,user_id)

#store the user's bookmarks in a list (stack implementation)
def store_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	key = "userId:%d:bookmarks" % (int(user_id))
	redis_obj.add_to_stack(key,bookmark_id)

#Retrieve methods
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

#A controller which calls the individual store methods
def store_bookmark(request,bookmark_form):
	redis_obj = Redis()
	bookmark_id = get_next_bookmarkId(redis_obj)
	store_url(redis_obj,bookmark_id,bookmark_form['url'])
	store_name(redis_obj,bookmark_id,bookmark_form['name'])
	store_description(redis_obj,bookmark_id,bookmark_form['description'])
	store_visibility(redis_obj,bookmark_id,bookmark_form['visibility'])
	store_created_date(redis_obj,bookmark_id,str(datetime.datetime.now()))
	store_userId(redis_obj,bookmark_id,get_userId(request))
	store_bookmark_uid_mapping(redis_obj,bookmark_id,get_userId(request))

#Get the user id by extracting auth token from cookies which is passed in the request
def get_userId(request):
	redis_obj = Redis()
	auth_token = request.COOKIES.get('auth','')

	key = "auth.token:%s:userId" %(auth_token)
	return redis_obj.get_value(key)

#View function which handles rendering the bookmark form 
#and stores them if valid or re-renders
def create_bookmark(request):
	
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
		data_dic['name'] = get_name(redis_obj, bookmark_id)
		data_dic['url'] = get_url(redis_obj, bookmark_id)
		data_dic['visibility'] = get_visibility(redis_obj, bookmark_id)
		data_dic['creation_date'] = get_creation_date(redis_obj, bookmark_id)
		data_dic['description'] = get_description(redis_obj, bookmark_id)

		data[i] = data_dic

	print data	
	return render_to_response('home.html', {'uid' : uid, 'bookmarks' : data})	