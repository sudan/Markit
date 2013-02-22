# Create your views here.
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext

from redis_helpers.views import Redis
from category.forms import CategoryForm
from auth.helpers import get_userId
from bookmark.bookmarks import store_category

def get_next_categoryId(redis_obj):
	''' Get the next category id '''

	key = "global:categoryId"
	return redis_obj.next_unique_key(key)

def category_name_exists(redis_obj,user_id,name):
	''' Check for the existence of a category '''

	key = "userId:%d:categoryName" %(int(user_id))
	return redis_obj.is_member_in_set(key,name)

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

def store_bookmark_category_mapping(redis_obj,user_id,category_id,bookmark_id):
	''' store the bookmark category user mapping 
	and add bookmark to categorized list '''

	key = "userId:%d:categoryId:%d:bookmarkId" %(int(user_id),category_id)
	redis_obj.add_to_set(key,bookmark_id)

	key = "userId:%d:categorized.bookmarks" %(int(user_id))
	redis_obj.add_to_set(key,bookmark_id)

def store_category_user(user_id,category_form):
	redis_obj = Redis()

	if category_name_exists(redis_obj,user_id,category_form['name']) == 0:
		category_id = get_next_categoryId()
		store_category_name(redis_obj,category_id,name)
		store_category_name_uid_mapping(redis_obj,user_id,category_id)
		store_category_name_uid_mapping(redis_obj,user_id,category_form['name'])

def create_category(request):
	''' create a new category '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request)

	if request.method == "POST":
		category_form = CategoryForm(data=request.POST)
		if category_form.is_valid():

			user_id = get_userId(request)
			store_category_user(user_id,category_form)
			category_form = category_form.cleaned_data
			return HttpResponseRedirect('/success/')

	category_form = CategoryForm()
	return render_to_response('category.html',{'category_form':category_form})

def add_bookmarks_to_category(request):
	''' add bookmark to category '''

	#yet to implement