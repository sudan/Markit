import random
import md5


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