# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

from redis_helpers.views import Redis
from auth.signin import login, authentication
from auth.login_status import is_logged_in
from auth.helpers import get_userId
from auth.getters import *

from online_bookmarking.settings import USERS_LIST_TEMPLATE_PATH
from socialize.profile import get_following_count,get_followers_count
import simplejson

def get_users(redis_obj, current_user_id):
	''' Returns the users excluding the current user '''
	
	key = "global:users:userId"
	user_ids = redis_obj.members_in_set(key)

	users_list = []
	for i, user_id in enumerate(user_ids):
		
		if int(user_id) != current_user_id:
			
			user_id = int(user_id)
			user_info = {}
			user_info['others_id'] = user_id
			user_info['email'] = get_email(redis_obj, user_id)
			user_info['username'] = get_username(redis_obj, user_id)
			user_info['first_name'] = get_first_name(redis_obj, user_id)
			user_info['last_name'] = get_last_name(redis_obj, user_id)
			user_info['description'] = get_summary(redis_obj,user_id)
			user_info['image_url'] = get_image_url(redis_obj, user_id)
			user_info['timestamp'] = get_timestamp(redis_obj, user_id)
			user_info['follow'] = is_following(redis_obj, current_user_id, user_id)
			user_info['followers'] = get_followers_count(redis_obj, user_id)
			user_info['following'] = get_following_count(redis_obj, user_id)

			users_list.append(user_info)
	
	return users_list

def get_followers(redis_obj, current_user_id):
	''' Returns the list of followers info  for the user id '''
	
	key = "userId:%d:followers" %(current_user_id)
	follower_ids = redis_obj.members_in_set(key)

	followers_list = [{} for i in xrange(len(follower_ids))]

	for i, follower_id in enumerate(follower_ids):

		follower_info = {}
		follower_id = int(follower_id)
		follower_info['others_id'] = follower_id
		follower_info['email'] = get_email(redis_obj, follower_id)
		follower_info['username'] = get_username(redis_obj, follower_id)
		follower_info['first_name'] = get_first_name(redis_obj, follower_id)
		follower_info['last_name'] = get_last_name(redis_obj, follower_id)
		follower_info['image_url'] = get_image_url(redis_obj, follower_id)
		follower_info['summary'] = get_summary(redis_obj,follower_id)
		follower_info['timestamp'] = get_timestamp(redis_obj, follower_id)	
		follower_info['relationship_status'] = is_following(redis_obj, current_user_id, follower_id)
		follower_info['following_count'] = get_following_count(redis_obj,follower_id)
		follower_info['followers_count'] = get_followers_count(redis_obj,follower_id)

		followers_list[i] = follower_info

	return followers_list

def get_following(redis_obj, current_user_id):
	''' Returns the users whom the user is following '''
	
	key = "userId:%d:following" %(current_user_id)
	
	following_ids = redis_obj.members_in_set(key)
	following_list = [{} for i in xrange(len(following_ids))]

	for i, following_id in enumerate(following_ids):

		following_info = {}
		following_id = int(following_id)
		following_info['others_id'] = following_id
		following_info['email'] = get_email(redis_obj, following_id)
		following_info['username'] = get_username(redis_obj, following_id)
		following_info['first_name'] = get_first_name(redis_obj, following_id)
		following_info['last_name'] = get_last_name(redis_obj, following_id)
		following_info['image_url'] = get_image_url(redis_obj, following_id)
		following_info['summary'] = get_summary(redis_obj,following_id)
		following_info['timestamp'] = get_timestamp(redis_obj, following_id)	
		following_info['relationship_status'] = True
		following_info['following_count'] = get_following_count(redis_obj,following_id)
		following_info['followers_count'] = get_followers_count(redis_obj,following_id)

		following_list[i] = following_info

	return following_list

def is_following(redis_obj, current_user_id, others_id):
	''' Returns true if the current user follows other user else false '''

	key = "userId:%d:following" %(current_user_id)
	result = redis_obj.is_member_in_set(key, others_id)
	if result == 1:
		return True
	else:
		return False

def follow_user(redis_obj, current_user_id, others_id):
	''' Add an entry in user's following list and other's followers list '''

	key = "userId:%d:following" %(current_user_id)
	redis_obj.add_to_set(key, others_id)

	key = "userId:%d:followers" %(others_id)
	redis_obj.add_to_set(key, current_user_id)

def unfollow_user(redis_obj, current_user_id, others_id):
	''' Remove the entry in user's following list and other's followers list '''

	key = "userId:%d:following" %(current_user_id)
	redis_obj.remove_from_set(key, others_id)

	key = "userId:%d:followers" %(others_id)
	redis_obj.remove_from_set(key, current_user_id)

@authentication('/users')
def toggle_relationship(request):
	''' Follow/unfollow a user '''

	current_user_id = get_userId(request)
	redis_obj = Redis()
	username = get_username(redis_obj, current_user_id)

	if request.method == "POST":

		if request.is_ajax():
			data = simplejson.loads(request.POST.keys()[0])
		else:
			data = request.POST

		others_id = data.get("others_id", "")
		relationship_request = data.get("relationship_request", "")
	
		if others_id != "" and relationship_request != "":

			if relationship_request == "follow":
				follow_user(redis_obj, current_user_id, int(others_id))
				toggle_status = "unfollow" 
			else:
				unfollow_user(redis_obj, current_user_id, int(others_id))
				toggle_status = "follow"

		data = {}
		try:
			
			data['status'] = 'success'
			data['toggle_status'] = toggle_status
			data['followers'] = get_followers_count(redis_obj,int(others_id))
			data['following'] = get_following_count(redis_obj,int(others_id))
		except:
			pass
		return HttpResponse(simplejson.dumps(data),mimetype='application/json')

	users_list = get_users(redis_obj, current_user_id)
	return render_to_response(USERS_LIST_TEMPLATE_PATH,
		{
			'users_list':users_list,
			'username':username,
		},
		context_instance=RequestContext(request))


@authentication('/users')
def users(request):
	''' Displays list of users '''

	current_user_id = get_userId(request)
	redis_obj = Redis()
	users_list = get_users(redis_obj, current_user_id)
	username = get_username(redis_obj, current_user_id)
	
	return render_to_response(USERS_LIST_TEMPLATE_PATH,
		{
			'users_list':users_list,
			'username':username,
		},
		context_instance=RequestContext(request))

def get_relations(request,relation_type,username):
	''' Display the followers or following depending on the request '''

	email = request.COOKIES.get("email", "")
	auth_token = request.COOKIES.get("auth", "")

	if not is_logged_in(email, auth_token):
		return login(request,'/relation/' + relation_type)

	redis_obj = Redis()
	
	try:
		user_id = get_unique_id(redis_obj,username)
		if relation_type == "followers":
			relations = get_followers(redis_obj,user_id)
		elif relation_type == "following":
			relations = get_following(redis_obj,user_id)
		else:
			relations = []
	except:
		relations = []

	return HttpResponse(simplejson.dumps(relations),mimetype='application/json')



