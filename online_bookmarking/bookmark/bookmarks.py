#change the name of the template
#update page after adding bookmarks
#if public add bookmarks to followers

from django.shortcuts import render_to_response, redirect
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext

import json
import datetime
from time import strftime

from bookmark.forms import BookmarkForm
from category.forms import CategoryForm
from tags.forms import TagForm
from redis_helpers.views import Redis
from auth.login_status import is_logged_in
from auth.signin import login, authentication
from auth.helpers import get_userId
from auth.getters import *
from tags.deleters import delete_bookmark_from_tag
from category.getters import get_category_for_user,get_categoryId_from_bookmark

from socialize.profile import get_user_info,get_following_count,get_followers_count

from bookmark.getters import *
from bookmark.setters import *
from bookmark.deleters import *
from django.utils import simplejson


from online_bookmarking.settings import BOOKMARK_ADD_TEMPLATE_PATH, HOME_TEMPLATE_PATH
from logger.get_logger import Logger

def store_bookmark(request, bookmark_form,edit_bookmark_id=''):
	''' A controller which calls the individual store methods '''

	redis_obj = Redis()

	#PUT and POST requests are handled in the same view
	if edit_bookmark_id != '':
		bookmark_id = int(edit_bookmark_id)
	else:
		bookmark_id = get_next_bookmarkId(redis_obj)
		store_created_date(redis_obj, bookmark_id, str(datetime.datetime.now()))
		store_bookmark_uid_mapping(redis_obj, bookmark_id, get_userId(request))
		store_userId(redis_obj, bookmark_id, get_userId(request))
	
	store_url(redis_obj, bookmark_id, bookmark_form['url'])
	store_name(redis_obj, bookmark_id, bookmark_form['name'])
	store_description(redis_obj, bookmark_id, bookmark_form['description'])
	store_visibility(redis_obj, bookmark_id, bookmark_form['visibility'])	

	return get_json_bookmark(redis_obj,bookmark_id)

def clear_bookmark(user_id, bookmark_id):
	''' Delete all mappings associated with bookmark id '''

	redis_obj = Redis()
	delete_url(redis_obj, bookmark_id)
	delete_name(redis_obj, bookmark_id)
	delete_description(redis_obj, bookmark_id)
	delete_visibility(redis_obj, bookmark_id)
	delete_created_date(redis_obj, bookmark_id)
	delete_userId(redis_obj, bookmark_id)
	delete_category(redis_obj, bookmark_id)
	delete_bookmark_uid_mapping(redis_obj, bookmark_id, user_id)
	delete_bookmark_from_tag(redis_obj,bookmark_id)
	
def get_bookmarks(request):

	redis_obj = Redis()
	user_id = get_userId(request)
	username = get_username(redis_obj, user_id)

	bookmarks = get_bookmark_uid_mapping_range(redis_obj, user_id, 0, 50)
	data = [{} for i in xrange(len(bookmarks))]
	
	for i, bookmark_id in enumerate(bookmarks):

		data_dic ={}
		bookmark_id = int(bookmark_id)
		data_dic['bookmark_id'] = bookmark_id
		data_dic['name'] = get_name(redis_obj, bookmark_id)
		data_dic['url'] = get_url(redis_obj, bookmark_id)
		data_dic['visibility'] = get_visibility(redis_obj, bookmark_id)
		data_dic['creation_date'] = get_created_date(redis_obj, bookmark_id).split()[0]
		data_dic['description'] = get_description(redis_obj, bookmark_id)
		data_dic['category_id'] = get_categoryId_from_bookmark(redis_obj,user_id,bookmark_id)
		
		data[i] = data_dic

	return username, data

@authentication('/bookmark')
def create_bookmark(request):
	''' View function which handles rendering the bookmark form and 
	stores them if valid or re-renders '''
	
	if request.method == "POST":
		
		if request.is_ajax():
			data = simplejson.loads(request.POST.keys()[0])
		else:
			data = request.POST
		
		bookmark_form = BookmarkForm(data=data)
		bookmark_id = data.get('bookmark_id','')
		if bookmark_id != '':
			bookmark_id = int(bookmark_id)

		if bookmark_form.is_valid():
			bookmark_form_cleaned = bookmark_form.cleaned_data
			bookmark_json = store_bookmark(request, bookmark_form_cleaned,bookmark_id)			
			return HttpResponse(bookmark_json, mimetype='application/json')

		bookmark_form.errors['status'] = 'failure'
		return HttpResponse(simplejson.dumps(bookmark_form.errors),mimetype='application/json')

	raise Http404()

@authentication('/home')
def display_bookmarks(request):
	''' Display existing bookmarks '''

	username , data = get_bookmarks(request)	
	bookmark_form = BookmarkForm(initial={'visibility':'public'})	
	category_form = CategoryForm()
	tag_form = TagForm()
	redis_obj = Redis()

	if request.is_ajax():
		
		data = simplejson.dumps(data)
		return HttpResponse(data, mimetype='application/json')

	user_info = get_user_info(redis_obj, username, get_userId(request))
	user_info['following'] = get_following_count(redis_obj, username)
	user_info['followers'] = get_followers_count(redis_obj, username)
	
	return render_to_response(HOME_TEMPLATE_PATH, 
		{
			'username' : username,
			'bookmark_form':bookmark_form,
			'category_form':category_form,
			'tag_form':tag_form,
			'user_info':user_info,
		},
		context_instance=RequestContext(request))	

@authentication('/home')
def delete_bookmark(request):
	''' Delete a bookmark '''

	bookmark_id = request.POST.get("bookmark_id", "")
	user_id = get_userId(request)

	if bookmark_id != "":
		clear_bookmark(user_id, int(bookmark_id))

	data  = {}	
	data ['status'] = 'success'
	return HttpResponse(simplejson.dumps(data),mimetype='application/json')