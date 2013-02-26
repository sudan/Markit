import hashlib
import md5
import datetime

def store_global_userIds(redis_obj,user_id):
	''' Store the list of user ids '''

	key = "global:users:userId"
	redis_obj.add_to_set(key,user_id)

def store_email(redis_obj,user_id,email):
	''' store the email id of the user '''
	
	key = "userId:%d:email" % (user_id)
	redis_obj.set_value(key,email)

def store_username(redis_obj,user_id,username):
	''' store the username of the user '''
	
	key = "userId:%d:username" % (user_id)
	redis_obj.set_value(key,username)

def store_first_name(redis_obj,user_id,first_name):
	''' store the first name of the user '''
	
	key = "userId:%d:first.name" % (user_id)
	redis_obj.set_value(key,first_name)

def store_last_name(redis_obj,user_id,last_name):
	''' store the last name of the user '''
	
	key = "userId:%d:last.name" % (user_id)
	redis_obj.set_value(key,last_name)

def store_password(redis_obj,user_id,password):
	''' store the password of the user '''
	
	key = "userId:%d:password" % (user_id)
	redis_obj.set_value(key,password)

def store_image_url(redis_obj,user_id,email):
	''' store the gravatar  image url of the user '''
	
	key = "userId:%d:image" %(user_id)
	image_url = "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(email).hexdigest()
	redis_obj.set_value(key,image_url)

def store_timestamp(redis_obj,user_id):
	''' store the timestamp of the user creation '''
	
	key = "userId:%d:timestamp" %(user_id)
	redis_obj.set_value(key,str(datetime.datetime.now()))

def store_uid_with_username(redis_obj,user_id,username):
	''' store the reverse mapping for the username '''
	
	key = "username:%s:userId" % (username)
	redis_obj.set_value(key,user_id)

def store_uid_with_email(redis_obj,user_id,email):
	''' store the reverse mapping for the email id '''
	
	key = "email:%s:userId" % (email)
	redis_obj.set_value(key,user_id)

def store_uid_with_auth_token(redis_obj,user_id,auth_token):
	''' store the reverse mapping for auth token '''
	
	key = "auth.token:%s:userId" % (auth_token)
	redis_obj.set_value(key,user_id)

def store_email_with_auth_token(redis_obj,email,auth_token):
	''' store the reverse mapping for auth token '''
	
	key = "auth.token:%s:email" % (auth_token)
	redis_obj.set_value(key,email)