# Create your views here.
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from redis_helpers.views import Redis
from category.forms import CategoryForm
from auth.helpers import get_userId
from auth.login_status import is_logged_in
from auth.signin import login
from bookmark.bookmarks import store_category

def get_next_categoryId(redis_obj):
	''' Get the next category id '''

	key = "global:categoryId"
	return redis_obj.next_unique_key(key)

def category_name_exists(redis_obj,user_id,name):
	''' Check for the existence of a category '''

	key = "userId:%d:categoryName" %(int(user_id))
	return redis_obj.is_member_in_set(key,name)

def get_category_name(redis_obj,user_id,name):
	''' return the category id given the user id and category name '''

	key = "userId:%d:categoryName:%s:categoryId" %(int(user_id),name)
	return redis_obj.get_value(key,category_id)

def store_category_name(redis_obj,category_id,name):
	''' store the category name '''

	key = "categoryId:%d:name" %(category_id)
	redis_obj.set_value(key,name)

def store_categoryId_uid_mapping(redis_obj,user_id,category_id):
	''' store the category id  associating it with the user '''

	key = "userId:%d:categoryId" %(int(user_id))
	redis_obj.add_to_set(key,category_id)

def store_category_name_uid_mapping(redis_obj,user_id,name):
	''' store the category name associating with the user '''

	key = "userId:%d:categoryName" %(int(user_id))
	redis_obj.add_to_set(key,name)

def store_category_name_userId_uid_mapping(redis_obj,user_id,category_id,name):
	''' store the category id corresponding to name and user Id '''

	key = "userId:%d:categoryName:%s:categoryId" %(int(user_id),name)
	redis_obj.set_value(key,category_id)

def store_bookmark_category_mapping(redis_obj,user_id,category_id,bookmark_id):
	''' store the bookmark category user mapping 
	and add bookmark to categorized list '''

	key = "userId:%d:bookmarkId:%d:categoryId" %(user_id,bookmark_id)
	if redis_obj.check_existence(key):
		old_category_id = int(redis_obj.get_value(key))
	else:
		old_category_id = None
	redis_obj.set_value(key,category_id)

	if  old_category_id != None:
		key = "userId:%d:categoryId:%d:bookmarkId" %(user_id,old_category_id)
		redis_obj.remove_from_set(key,bookmark_id) 
	
	key = "userId:%d:categoryId:%d:bookmarkId" %(user_id,category_id)
	redis_obj.add_to_set(key,bookmark_id)


	key = "userId:%d:categorized.bookmarks" %(user_id)
	redis_obj.add_to_set(key,bookmark_id)


def store_category_user(user_id,category_form):
	''' A controller which calls remaining methods for creating 
	a new category '''

	redis_obj = Redis()

	if category_name_exists(redis_obj,user_id,category_form['name']) == 0:
		category_id = get_next_categoryId(redis_obj)
		store_category_name(redis_obj,category_id,category_form['name'])
		store_categoryId_uid_mapping(redis_obj,user_id,category_id)
		store_category_name_uid_mapping(redis_obj,user_id,category_form['name'])
		store_category_name_userId_uid_mapping(redis_obj,user_id,category_id,category_form['name'])

def create_category(request):
	''' create a new category '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request)

	if request.method == "POST":
		category_form = CategoryForm(data=request.POST)
		if category_form.is_valid():

			category_form = category_form.cleaned_data
			user_id = get_userId(request)
			store_category_user(user_id,category_form)
	
			return HttpResponseRedirect('/success/')

	category_form = CategoryForm()
	return render_to_response('category.html',{'category_form':category_form},
		context_instance=RequestContext(request))

def add_bookmarks_to_category(request):
	''' add bookmark to category '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request)


	if request.method == "POST":
		bookmark_id = request.POST.get("bookmark_id","")
		category_id = request.POST.get("category_id","")

		redis_obj = Redis()
		store_bookmark_category_mapping(redis_obj,int(get_userId(request)),int(category_id),int(bookmark_id))

		return HttpResponseRedirect('/success/')

	return render_to_response('add_bookmarks_to_category.html',context_instance=RequestContext(request))


