from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import Http404

from redis_helpers.views import Redis
from auth.signin import login,authentication
from auth.login_status import is_logged_in
from auth.helpers import get_userId
from auth.getters import *
from bookmark.getters import *

def is_following(redis_obj,current_user_id,others_id):
	''' Returns true if the current user follows other user else false '''

	key = "userId:%d:following" %(current_user_id)
	result = redis_obj.is_member_in_set(key,others_id)
	if result == 1:
		return True
	else:
		return False

def get_user_info(redis_obj,profile_name,current_user_id):
	''' Returns the profile info about the user '''

	user_id = get_unique_id(redis_obj,profile_name)
	user_info = {}
	user_info['others_id'] = user_id
	user_info['email'] = get_email(redis_obj,user_id)
	user_info['username'] = get_username(redis_obj,user_id)
	user_info['first_name'] = get_first_name(redis_obj,user_id)
	user_info['last_name'] = get_last_name(redis_obj,user_id)
	user_info['image_url'] = get_image_url(redis_obj,user_id)
	user_info['timestamp'] = get_timestamp(redis_obj,user_id)
	user_info['follow'] = is_following(redis_obj,current_user_id,user_id)

	return user_info

def get_following_count(redis_obj,profile_name):
	''' Returns the following count of the user '''

	user_id = get_unique_id(redis_obj,profile_name)

	key = "userId:%d:following" %(user_id)
	return redis_obj.total_members(key)

def get_followers_count(redis_obj,profile_name):
	''' Returns the followers count of the user '''

	user_id = get_unique_id(redis_obj,profile_name)

	key = "userId:%d:followers" %(user_id)
	return redis_obj.total_members(key)

def get_public_bookmarks(redis_obj,profile_name):
	''' Return the public bookmarks of the user '''

	user_id = get_unique_id(redis_obj,profile_name)
	
	key = "userId:%d:bookmarks" %(user_id)
	bookmark_ids = redis_obj.get_elements_in_range(key,0,25)

	bookmarks_list = []
	for i,bookmark_id in enumerate(bookmark_ids):
		bookmark_info = {}
		if get_visibility(redis_obj,int(bookmark_id)) == "private":
			continue
		bookmark_info['url'] = get_url(redis_obj,int(bookmark_id))
		bookmark_info['name'] = get_name(redis_obj,int(bookmark_id))
		bookmark_info['description'] = get_description(redis_obj,int(bookmark_id))
		bookmark_info['created_date'] = get_created_date(redis_obj,int(bookmark_id))
		bookmarks_list.append(bookmark_info)
		
	return bookmarks_list

@authentication('/users')
def profile(request,profile_name=''):
	''' profile for a user '''

	current_user_id = get_userId(request)
	
	if profile_name != '':
		redis_obj = Redis()
		user_id = get_unique_id(redis_obj,profile_name)
		
		user_info = get_user_info(redis_obj,profile_name,user_id)
		followers_count = get_followers_count(redis_obj,profile_name)
		following_count = get_following_count(redis_obj,profile_name)
		public_bookmarks = get_public_bookmarks(redis_obj,profile_name)

		if user_id == current_user_id:
			my_profile = True
		else:
			my_profile = False
		
		follow = is_following(redis_obj,current_user_id,user_id)

		return render_to_response('profile.html',
			{
				'user_info':user_info,
				'followers_count':followers_count,
				'following_count':following_count,
				'public_bookmarks':public_bookmarks,
				'my_profile':my_profile,
				'follow': follow
			},
			context_instance=RequestContext(request))

	return Http404()