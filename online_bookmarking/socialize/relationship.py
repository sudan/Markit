# Create your views here.
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

from redis_helpers.views import Redis
from auth.signin import login,authentication
from auth.login_status import is_logged_in
from auth.helpers import get_userId
from auth.getters import *

from online_bookmarking.settings import USERS_LIST_TEMPLATE_PATH

def get_users(redis_obj,current_user_id):
	''' Returns the users excluding the current user '''
	
	key = "global:users:userId"
	user_ids = redis_obj.members_in_set(key)

	users_list = []
	for i, user_id in enumerate(user_ids):
		
		if int(user_id) != current_user_id:
			
			user_id = int(user_id)
			user_info = {}
			user_info['others_id'] = user_id
			user_info['email'] = get_email(redis_obj,user_id)
			user_info['username'] = get_username(redis_obj,user_id)
			user_info['first_name'] = get_first_name(redis_obj,user_id)
			user_info['last_name'] = get_last_name(redis_obj,user_id)
			user_info['image_url'] = get_image_url(redis_obj,user_id)
			user_info['timestamp'] = get_timestamp(redis_obj,user_id)
			user_info['follow'] = is_following(redis_obj,current_user_id,user_id)

			users_list.append(user_info)
	
	return users_list

def get_followers(redis_obj,current_user_id):
	''' Returns the list of followers info  for the user id '''
	
	key = "userId:%d:followers" %(current_user_id)
	follower_ids = redis_obj.members_in_set(current_user_id)

	followers_list = [{} for i in xrange(len(follower_ids))]

	for i, follower_id in enumerate(follower_ids):

		follower_info = {}
		follower_info['others_id'] = follower_id
		follower_info['email'] = get_email(redis_obj,follower_id)
		follower_info['username'] = get_username(redis_obj,follower_id)
		follower_info['first_name'] = get_first_name(redis_obj,follower_id)
		follower_info['last_name'] = get_last_name(redis_obj,follower_id)
		follower_info['image_url'] = get_image_url(redis_obj,follower_id)
		follower_info['timestamp'] = get_timestamp(redis_obj,follower_id)	
		follower_info['follow'] = is_following(redis_obj,current_user_id,follower_id)

		followers_list[i] = follower_info

	return followers_list

def get_following(redis_obj,current_user_id):
	''' Returns the users whom the user is following '''
	
	key = "userId:%d:following" %(current_user_id)
	following_ids = redis_obj.members_in_set(current_user_id)

	following_list = [{} for i in xrange(len(following_ids))]

	for i, following_id in enumerate(following_ids):

		following_info = {}
		following_info['others_id'] = following_id
		following_info['email'] = get_email(redis_obj,following_id)
		following_info['username'] = get_username(redis_obj,following_id)
		following_info['first_name'] = get_first_name(redis_obj,following_id)
		following_info['last_name'] = get_last_name(redis_obj,following_id)
		following_info['image_url'] = get_image_url(redis_obj,following_id)
		following_info['timestamp'] = get_timestamp(redis_obj,following_id)	
		following_info['follow'] = True

		following_list[i] = following_info

	return following_list

def is_following(redis_obj,current_user_id,others_id):
	''' Returns true if the current user follows other user else false '''

	key = "userId:%d:following" %(current_user_id)
	result = redis_obj.is_member_in_set(key,others_id)
	if result == 1:
		return True
	else:
		return False

def follow_user(redis_obj,current_user_id,others_id):
	''' Add an entry in user's following list and other's followers list '''

	key = "userId:%d:following" %(current_user_id)
	redis_obj.add_to_set(key,others_id)

	key = "userId:%d:followers" %(others_id)
	redis_obj.add_to_set(key,current_user_id)

def unfollow_user(redis_obj,current_user_id,others_id):
	''' Remove the entry in user's following list and other's followers list '''

	key = "userId:%d:following" %(current_user_id)
	redis_obj.remove_from_set(key,others_id)

	key = "userId:%d:followers" %(others_id)
	redis_obj.remove_from_set(key,current_user_id)

@authentication('/users')
def toggle_relationship(request):
	''' Follow a user '''

	current_user_id = get_userId(request)
	
	if request.method == "POST":

		others_id = request.POST.get("others_id","")
		relationship_request = request.POST.get("relationship_button","")
		
		if others_id != "" and relationship_request != "":

			redis_obj = Redis()
			if relationship_request == "follow":
				follow_user(redis_obj,current_user_id,int(others_id)) 
			else:
				unfollow_user(redis_obj,current_user_id,int(others_id))

	current_user_id = get_userId(request)
	redis_obj = Redis()
	users_list = get_users(redis_obj,current_user_id)

	return render_to_response(USERS_LIST_TEMPLATE_PATH,
		{
			'users_list':users_list
		},
		context_instance=RequestContext(request))

@authentication('/users')
def users(request):
	''' Displays list of users '''

	current_user_id = get_userId(request)
	redis_obj = Redis()
	users_list = get_users(redis_obj,current_user_id)
	
	return render_to_response(USERS_LIST_TEMPLATE_PATH,
		{
			'users_list':users_list
		},
		context_instance=RequestContext(request))

