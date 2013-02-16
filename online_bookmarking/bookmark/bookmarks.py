#todos -- append the uid of the user

from django.shortcuts import render_to_response
from django.http import  Http404,HttpResponseRedirect,HttpResponse
from django.template import RequestContext

import json
import datetime

from bookmark.forms import BookmarkForm
from redis_helpers.views import Redis

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
	key = "bookmarkId:%d:created_date" % (bookmark_id)
	redis_obj.set_value(key,created_date)

#A controller which calls the individual store methods
def store_bookmark(bookmark_form):
	redis_obj = Redis()
	bookmark_id = get_next_bookmarkId(redis_obj)
	store_url(redis_obj,bookmark_id,bookmark_form['url'])
	store_name(redis_obj,bookmark_id,bookmark_form['name'])
	store_description(redis_obj,bookmark_id,bookmark_form['description'])
	store_visibility(redis_obj,bookmark_id,bookmark_form['visibility'])
	store_created_date(redis_obj,bookmark_id,str(datetime.datetime.now()))

#View function which handles rendering the bookmark form and stores them if valid or re-renders
def create_bookmark(request):
	
	if request.method == "POST":

		bookmark_form = BookmarkForm(data=request.POST)
		
		if bookmark_form.is_valid():
			bookmark_form = bookmark_form.cleaned_data
			store_bookmark(bookmark_form)
			return HttpResponseRedirect('/success/')

		return render_to_response('home.html',{'bookmark_form':bookmark_form},context_instance=RequestContext(request))

	bookmark_form = BookmarkForm()
	return render_to_response('home.html',{'bookmark_form':bookmark_form},context_instance=RequestContext(request))

