from redis_helpers.views import Redis

def get_next_bookmarkId(redis_obj):
	''' Get the next unique bookmark id '''

	key = "global:bookmarkId"
	return Redis.next_unique_key(redis_obj,key)

def get_url(redis_obj, bookmark_id):
	''' Retrieve bookmark URL '''

	key = "bookmarkId:%d:url" % (bookmark_id)
	return redis_obj.get_value(key)

def get_name(redis_obj, bookmark_id):
	''' Retrieve bookmark name '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	return redis_obj.get_value(key)

def get_description(redis_obj, bookmark_id):
	''' Retrieve bookmark description '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	return redis_obj.get_value(key)

def get_visibility(redis_obj, bookmark_id):
	''' Retrieve bookmark visibility '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	return redis_obj.get_value(key)

def get_created_date(redis_obj, bookmark_id):
	''' Retrieve bookmark creation time '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	return redis_obj.get_value(key)

def get_bookmark_uid_mapping_all(redis_obj, user_id):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_elements_in_range(key)

def get_bookmark_uid_mapping_range(redis_obj, user_id, start, end):
	''' Retrieve the user's bookmark ids '''

	key = "userId:%d:bookmarks" % (int(user_id))
	return redis_obj.get_elements_in_range(key, start, end)