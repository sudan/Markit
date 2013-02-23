from redis_helpers.views import Redis

def remove_category_name_userId_uid_mapping(redis_obj,user_id,name):
	''' remove the mapping to update the category name '''

	key = "userId:%d:categoryName:%s:categoryId" %(int(user_id),name)
	redis_obj.remove_key(key)