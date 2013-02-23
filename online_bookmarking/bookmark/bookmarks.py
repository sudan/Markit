#change the name of the template
#update page after adding bookmarks
#blocked coz of auth module
#if public add bookmarks to followers
#once signed in should be redirected to corresponding page
#add bookmark to tags

from django.shortcuts import render_to_response
from django.http import  Http404,HttpResponseRedirect,HttpResponse
from django.template import RequestContext

import json
import datetime

from bookmark.forms import BookmarkForm
from redis_helpers.views import Redis
from auth.login_status import is_logged_in
from auth.signin import login
from auth.helpers import get_userId

def get_next_bookmarkId(redis_obj):
	''' Get the next unique bookmark id '''

	key = "global:bookmarkId"
	return Redis.next_unique_key(redis_obj,key)

def store_url(redis_obj,bookmark_id,url):
	''' Store the url of the bookmark '''  

	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.set_value(key,url)

def get_url(redis_obj, bookmark_id):
	''' Retrieve bookmark URL '''

	key = "bookmarkId:%d:url" % (bookmark_id)
	return redis_obj.get_value(key)

def delete_url(redis_obj,bookmark_id):
	''' Delete the bookmark url '''

	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.remove_key(key)

def store_name(redis_obj,bookmark_id,name):
	''' store the name of the bookmark '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.set_value(key,name)

def get_name(redis_obj, bookmark_id):
	''' Retrieve bookmark name '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	return redis_obj.get_value(key)

def delete_name(redis_obj,bookmark_id):
	''' Delete the bookmark name '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.remove_key(key)

def store_description(redis_obj,bookmark_id,description):
	''' store the description of the bookmark '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.set_value(key,description)

def get_description(redis_obj, bookmark_id):
	''' Retrieve bookmark description '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	return redis_obj.get_value(key)

def delete_description(redis_obj,bookmark_id):
	''' Delete the bookmark description '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.remove_key(key)

def store_visibility(redis_obj,bookmark_id,visibility):
	''' store the visibility of bookmark '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.set_value(key,visibility)

def get_visibility(redis_obj, bookmark_id):
	''' Retrieve bookmark visibility '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	return redis_obj.get_value(key)

def delete_visibility(redis_obj,bookmark_id):
	''' Delete the bookmark visibility '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.remove_key(key)

def store_created_date(redis_obj,bookmark_id,created_date):
	''' store the creation time of bookmark '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.set_value(key,created_date)

def get_created_date(redis_obj, bookmark_id):
	''' Retrieve bookmark creation time '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	return redis_obj.get_value(key)

def delete_created_date(redis_obj,bookmark_id):
	''' Delete the bookmark created date '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.remove_key(key)

def store_userId(redis_obj,bookmark_id,user_id):
	''' store the user id in the bookmark '''

	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.set_value(key,user_id)

def delete_userId(redis_obj,bookmark_id):
	''' Delete the bookmark user id mapping '''

	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.remove_key(key)

def store_category(redis_obj,bookmark_id,category_id):
	''' store the category bookmark association '''

	key = "bookmarkId:%d:categoryId" %(bookmark_id)
	redis_obj.set_value(key,category_id)

def delete_category(redis_obj,bookmark_id):
	''' Delete the bookmark category mapping '''

	key = "bookmarkId:%d:categoryId" % (bookmark_id)
	redis_obj.remove_key(key)

def store_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	''' store the user's bookmarks in a list (stack implementation) '''

	key = "userId:%d:bookmarks" % (int(user_id))
	redis_obj.add_to_stack(key,bookmark_id)

def get_bookmark_uid_mapping_all(redis_obj, user_id):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_elements_in_range(key)

def delete_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	''' Remove bookmark id from user id mapping ''' 

	key = "userId:%d:bookmarks" %(int(user_id))
	redis_obj.remove_from_stack(key,0,value)

def get_bookmark_uid_mapping_range(redis_obj, user_id, start, end):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_elements_in_range(key, start, end)

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

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")
	if not is_logged_in(email,auth_token):
		return login(request)

	uid , data = get_bookmarks(request)		

	return render_to_response('home.html', {'uid' : uid, 'bookmarks' : data})	

def delete_bookmark(request):
	''' Delete a bookmark '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")
	if not is_logged_in(email,auth_token):
		return login(request)

	bookmark_id = request.POST.get("bookmark_id","")
	user_id = get_userId(request)

	if bookmark_id != "":
		clear_bookmark(int(user_id),int(bookmark_id))