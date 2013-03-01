from redis_helpers.views import Redis

def store_url(redis_obj,bookmark_id,url):
	''' Store the url of the bookmark '''  

	key = "bookmarkId:%d:url" % (bookmark_id)
	redis_obj.set_value(key,url)

def store_name(redis_obj,bookmark_id,name):
	''' store the name of the bookmark '''

	key = "bookmarkId:%d:name" % (bookmark_id)
	redis_obj.set_value(key,name)

def store_description(redis_obj,bookmark_id,description):
	''' store the description of the bookmark '''

	key = "bookmarkId:%d:description" % (bookmark_id)
	redis_obj.set_value(key,description)

def store_visibility(redis_obj,bookmark_id,visibility):
	''' store the visibility of bookmark '''

	key = "bookmarkId:%d:visibility" % (bookmark_id)
	redis_obj.set_value(key,visibility)

def store_created_date(redis_obj,bookmark_id,created_date):
	''' store the creation time of bookmark '''

	key = "bookmarkId:%d:created.date" % (bookmark_id)
	redis_obj.set_value(key,created_date)

def store_userId(redis_obj,bookmark_id,user_id):
	''' store the user id in the bookmark '''

	key = "bookmarkId:%d:userId" % (bookmark_id)
	redis_obj.set_value(key,user_id)

def store_category(redis_obj,bookmark_id,category_id):
	''' store the category bookmark association '''

	key = "bookmarkId:%d:categoryId" %(bookmark_id)
	redis_obj.set_value(key,category_id)

def store_bookmark_uid_mapping(redis_obj,bookmark_id,user_id):
	''' store the user's bookmarks in a list (stack implementation) '''

	key = "userId:%d:bookmarks" % (user_id)
	redis_obj.add_to_stack(key,bookmark_id)