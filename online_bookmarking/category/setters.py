from redis_helpers.views import Redis

def store_category_name(redis_obj,category_id,name):
	''' store the category name '''

	key = "categoryId:%d:name" %(category_id)
	redis_obj.set_value(key,name)

def store_categoryId_uid_mapping(redis_obj,user_id,category_id):
	''' store the category id  associating it with the user '''

	key = "userId:%d:categoryId" %(user_id)
	redis_obj.add_to_set(key,category_id)

def store_category_name_uid_mapping(redis_obj,user_id,name):
	''' store the category name associating with the user '''

	key = "userId:%d:categoryName" %(user_id)
	redis_obj.add_to_set(key,name)

def store_category_name_userId_uid_mapping(redis_obj,user_id,category_id,name):
	''' store the category id corresponding to name and user Id '''

	key = "userId:%d:categoryName:%s:categoryId" %(user_id,name)
	redis_obj.set_value(key,category_id)

