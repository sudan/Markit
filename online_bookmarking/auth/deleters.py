def delete_uid_with_username(redis_obj, username):
	''' remove the reverse mapping for the username '''
	
	key = "username:%s:userId" % (username)
	redis_obj.remove_key(key)

def delete_uid_with_email(redis_obj, email):
	''' remove the reverse mapping for the email id '''
	
	key = "email:%s:userId" % (email)
	redis_obj.remove_key(key)

