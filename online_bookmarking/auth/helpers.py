import random
import md5

from redis_helpers.views import Redis

def get_auth_token():
	''' Get auth token '''

	random_range = random.randrange(0,65535)
	m = md5.new()
	m.update(str(random_range))
	return m.hexdigest()

def store_auth_token(redis_obj,user_id,email,auth_token):
	''' store auth token of the user '''
	
	key = "userId:%d:auth.token" %(user_id)
	redis_obj.set_value(key,auth_token)

	key = "email:%s:auth.token" %(email)
	redis_obj.set_value(key,auth_token)

def get_userId(request):
	''' Get the user id by extracting auth token from cookies which is passed in the request '''

	redis_obj = Redis()
	auth_token = request.COOKIES.get('auth','')

	key = "auth.token:%s:userId" %(auth_token)
	return int(redis_obj.get_value(key))