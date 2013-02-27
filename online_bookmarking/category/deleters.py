from redis_helpers.views import Redis
from category.getters import get_category_name

def remove_category_name_userId_uid_mapping(redis_obj,user_id,name):
	''' remove the mapping to update the category name '''

	key = "userId:%d:categoryName:%s:categoryId" %(user_id,name)
	redis_obj.remove_key(key)

def delete_category_name(redis_obj,category_id):
	''' delete the category name '''

	key = "categoryId:%d:name" %(category_id)
	redis_obj.remove_key(key)

def delete_categoryId_uid_mapping(redis_obj,user_id,category_id):
	''' delete the category id  associating it with the user '''

	key = "userId:%d:categoryId" %(user_id)
	redis_obj.remove_from_set(key,category_id)

def delete_category_name_uid_mapping(redis_obj,user_id,category_id):
	''' delete the category name associating with the user '''

	name = get_category_name(category_id)
	key = "userId:%d:categoryName" %(user_id)
	redis_obj.remove_from_set(key,name)

def delete_category_name_userId_uid_mapping(redis_obj,user_id,category_id):
	''' delete the category id corresponding to name and user Id '''

	name = get_category_name(category_id)
	key = "userId:%d:categoryName:%s:categoryId" %(user_id,name)
	redis_obj.remove_key(key)