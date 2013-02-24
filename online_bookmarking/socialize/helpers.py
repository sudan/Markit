def is_following(redis_obj,current_user_id,others_id):
	''' Returns true if the current user follows other user else false '''

	key = "userId:%d:following" %(current_user_id)
	result = redis_obj.is_member_in_set(key,others_id)
	if result == 1:
		return True
	else:
		return False

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
		follower_info['follow'] = is_following(redis_obj,int(current_user_id),int(follower_id))

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

def get_following_count(redis_obj,profile_name):
	''' Returns the following count of the user '''

	user_id = get_unique_id(redis_obj,profile_name)

	key = "userId:%d:following" %(int(user_id))
	return redis_obj.total_members(key)

def get_followers_count(redis_obj,profile_name):
	''' Returns the followers count of the user '''

	user_id = get_unique_id(redis_obj,profile_name)

	key = "userId:%d:followers" %(int(user_id))
	return redis_obj.total_members(key)