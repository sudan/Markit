def get_email(redis_obj,user_id):
	''' get the email id of the user '''
	
	key = "userId:%d:email" % (user_id)
	return redis_obj.get_value(key)

def get_username(redis_obj,user_id):
	''' get the username of the user '''
	
	key = "userId:%d:username" % (user_id)
	return redis_obj.get_value(key)

def get_first_name(redis_obj,user_id):
	''' get the first name of the user '''
	
	key = "userId:%d:first.name" % (user_id)
	return redis_obj.get_value(key)

def get_last_name(redis_obj,user_id):
	''' get the last name of the user '''
	
	key = "userId:%d:last.name" % (user_id)
	return redis_obj.get_value(key)

def get_image_url(redis_obj,user_id):
	''' get the gravatar  image url of the user '''
	
	key = "userId:%d:image" %(user_id)
	return redis_obj.get_value(key)

def get_timestamp(redis_obj,user_id):
	''' get the timestamp of the user creation '''
	
	key = "userId:%d:timestamp" %(user_id)
	return redis_obj.get_value(key)

def get_unique_id(redis_obj,username):
	''' get the user id given the username '''

	key = "username:%s:userId" %(username)
	return int(redis_obj.get_value(key))

def get_password(redis_obj,user_id):
	''' get the password of the user '''

	key = "userId:%d:password" %(user_id)
	return redis_obj.get_value(key)

def get_auth_token(redis_obj,user_id):
	''' get the auth token of the user '''

	key = "userId:%d:auth.token" %(user_id)
	return redis_obj.get_value(key)