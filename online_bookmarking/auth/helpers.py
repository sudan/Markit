import random
import md5

#Get auth token
def get_auth_token():
	random_range = random.randrange(0,65535)
	m = md5.new()
	m.update(str(random_range))
	return m.digest()

#store auth token of the user
def store_auth_token(redis_obj,user_id,auth_token):
	key = "userId:%d:auth.token" %(user_id)
	redis_obj.set_value(key,auth_token)