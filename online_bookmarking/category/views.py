# Create your views here.
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse

from redis_helpers.views import Redis
from category.forms import CategoryForm
from auth.helpers import get_userId
from auth.login_status import is_logged_in
from auth.signin import login, authentication
from bookmark.bookmarks import store_category

from category.getters import *
from category.setters import *
from category.deleters import *

import simplejson

from online_bookmarking.settings import CATEGORY_CREATE_TEMPLATE_PATH
from online_bookmarking.settings import ADD_BOOKMARKS_TO_CATEGORY_TEMPLATE_PATH
from online_bookmarking.settings import HOME_TEMPLATE_PATH

def category_name_exists(redis_obj, user_id, name):
	''' Check for the existence of a category '''

	key = "userId:%d:categoryName" %(user_id)
	return redis_obj.is_member_in_set(key, name)

def store_bookmark_category_mapping(redis_obj, user_id, category_id, bookmark_id):
	''' store the bookmark category user mapping 
	and add bookmark to categorized list '''

	key = "userId:%d:categoryId" %(user_id)
	value = category_id

	if redis_obj.is_member_in_set(key, value) == 1:
		
		key = "userId:%d:bookmarkId:%d:categoryId" %(user_id, bookmark_id)
		if redis_obj.check_existence(key):
			old_category_id = int(redis_obj.get_value(key))
		else:
			old_category_id = None
		redis_obj.set_value(key, category_id)

		if  old_category_id != None:
			key = "userId:%d:categoryId:%d:bookmarkId" %(user_id, old_category_id)
			redis_obj.remove_from_set(key, bookmark_id) 
	
		key = "userId:%d:categoryId:%d:bookmarkId" %(user_id, category_id)
		redis_obj.add_to_set(key, bookmark_id)

		key = "userId:%d:categorized.bookmarks" %(user_id)
		redis_obj.add_to_set(key, bookmark_id)

def store_category_user(user_id, category_form):
	''' A controller which calls remaining methods for creating 
	a new category '''

	redis_obj = Redis()
	status = 'success'

	#POST and PUT requests handled in the same view
	if category_name_exists(redis_obj, user_id, category_form['name']) == 0:
		category_id = get_next_categoryId(redis_obj)
		store_category_name(redis_obj, category_id, category_form['name'])
		store_categoryId_uid_mapping(redis_obj, user_id, category_id)
		store_category_name_uid_mapping(redis_obj, user_id, category_form['name'])
		store_category_name_userId_uid_mapping(redis_obj, user_id, category_id, category_form['name'])
	else:
		status = 'duplicate'
		category_id = category_form.get('category_id', '')
		if category_id == '':
			pass
		else:
			category_id = int(category_id)
			old_category_name = get_category_name(redis_obj, category_id)
			store_category_name(redis_obj, category_id, category_form['name'])
			store_category_name_uid_mapping(redis_obj, user_id, category_form['name'])
			remove_category_name_userId_uid_mapping(redis_obj, user_id, old_category_name)
			store_category_name_userId_uid_mapping(redis_obj, user_id, category_id, category_form['name'])

	category = {}
	category['category_id'] = category_id
	category['category_name'] = category_form['name']
	category['status'] = status
	return simplejson.dumps(category) 

@authentication('/category')
def create_category(request):
	''' create a new category '''

	if request.method == "POST":

		if request.is_ajax():
			data = simplejson.loads(request.POST.keys()[0])
		else:
			data = request.POST
		
		category_form = CategoryForm(data=data)
		
		if category_form.is_valid():

			category_form_cleaned = category_form.cleaned_data
			user_id = get_userId(request)
			category_json = store_category_user(user_id, category_form_cleaned)
		
			return HttpResponse(category_json, mimetype='application/json')

		category_form.errors['status'] = 'failure'
		return HttpResponse(simplejson.dumps(category_form.errors),mimetype='application/json')

	raise Http404()

@authentication('/categories')
def get_categories(request):
	''' Get the categories of the user '''

	redis_obj = Redis()
	data = simplejson.dumps(get_category_for_user(redis_obj, get_userId(request)))
	return HttpResponse(data, mimetype='application/json')
	
@authentication('/add_bookmarks_to_category')
def add_bookmarks_to_category(request):
	''' add bookmark to category '''

	if request.method == "POST":
		bookmark_id = request.POST.get("bookmark_id", "")
		category_id = request.POST.get("category_id", "")
		user_id = get_userId(request)

		redis_obj = Redis()

		store_bookmark_category_mapping(redis_obj, get_userId(request), int(category_id), int(bookmark_id))

		return HttpResponseRedirect('/success/')

	return render_to_response(ADD_BOOKMARKS_TO_CATEGORY_TEMPLATE_PATH,
		context_instance=RequestContext(request))

@authentication('/home')
def clear_category(request):
	''' clear the category '''

	if request.method == "POST":
		user_id = get_userId(request)
		category_id = request.POST.get("category_id", "")

		redis_obj = Redis()
		delete_category_name(redis_obj, category_id)
		delete_categoryId_uid_mapping(redis_obj, user_id, category_id)
		delete_category_name_uid_mapping(redis_obj, user_id, category_id)
		delete_category_name_userId_uid_mapping(redis_obj, user_id, category_id)

	return render_to_response(HOME_TEMPLATE_PATH,
		context_instance=RequestContext(request))


