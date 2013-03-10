from redis_helpers.views import Redis

def get_next_categoryId(redis_obj):
	''' Get the next category id '''

	key = "global:categoryId"
	return redis_obj.next_unique_key(key)

def get_categoryId(redis_obj, user_id, name):
	''' return the category id given the user id and category name '''

	key = "userId:%d:categoryName:%s:categoryId" %(user_id, name)
	return int(redis_obj.get_value(key))

def get_categoryId_from_bookmark(redis_obj,user_id,bookmark_id):
	''' Returns the category id given the user id and bookmark id '''

	key = "userId:%d:bookmarkId:%d:categoryId" %(user_id,bookmark_id)
	value = redis_obj.get_value(key)
	if value is None:
		return 0;
	else:
		return value;

def get_category_name(redis_obj, category_id):
	''' return the category name given the id '''

	key = "categoryId:%d:name" %(category_id)
	return redis_obj.get_value(key)

def get_category_for_user(redis_obj,user_id):
	''' returns the json with id as key and name as value '''

	key = "userId:%d:categoryId" %(user_id)
	category_ids = redis_obj.members_in_set(key)

	categories = [{} for i in xrange(len(category_ids))]

	for i,category_id in enumerate(category_ids):
		category = {}
		category_name = get_category_name(redis_obj,int(category_id))
		category['category_id'] = category_id
		category['name'] = category_name
		categories[i] = category

	return categories