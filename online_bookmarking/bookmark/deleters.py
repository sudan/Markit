from redis_helpers.views import Redis

def delete_url(redis_obj,bookmark_id):
	''' Delete the bookmark url '''

	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_name(redis_obj,bookmark_id):
	''' Delete the bookmark name '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_description(redis_obj,bookmark_id):
	''' Delete the bookmark description '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_visibility(redis_obj,bookmark_id):
	''' Delete the bookmark visibility '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_created_date(redis_obj,bookmark_id):
	''' Delete the bookmark created date '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_userId(redis_obj,bookmark_id):
	''' Delete the bookmark user id mapping '''

	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_category(redis_obj,bookmark_id):
	''' Delete the bookmark category mapping '''

	key = "bookmarkId:%d:categoryId" % (bookmark_id)
	redis_obj.remove_key(key)

def delete_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	''' Remove bookmark id from user id mapping ''' 

	key = "userId:%d:bookmarks" %(int(user_id))
	redis_obj.remove_from_stack(key,0,value)