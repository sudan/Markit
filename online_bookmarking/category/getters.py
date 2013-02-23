from redis_helpers.views import Redis

def get_next_categoryId(redis_obj):
	''' Get the next category id '''

	key = "global:categoryId"
	return redis_obj.next_unique_key(key)

def get_categoryId(redis_obj,user_id,name):
	''' return the category id given the user id and category name '''

	key = "userId:%d:categoryName:%s:categoryId" %(int(user_id),name)
	return redis_obj.get_value(key,category_id)

def get_category_name(redis_obj,category_id):
	''' return the category name given the id '''

	key = "categoryId:%d:name" %(category_id)
	return redis_obj.get_value(key)