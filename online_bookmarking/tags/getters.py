from redis_helpers.views import Redis

def get_next_tagId(redis_obj):
	''' Get the next unique tag id '''
	
	key = "global:tagId"
	return redis_obj.next_unique_key(key)

def get_bookmark_list(data):
	''' Function which returns id value format of bookmarks
	suitable for multi select dropdown '''

	return tuple([(i['bookmark_id'],i['name']) for i in data])

def get_global_tagIds(redis_obj):
	''' Function which returns all the tag ids '''

	key = "global:tags:tagId"
	redis_obj.members_in_set(key)

def get_tag_name(redis_obj,tag_id):
	''' Function which returns the name for the tag id '''

	key = "tagId:%d:name" %(tag_id)
	return redis_obj.get_value(key)

def bookmark_for_tags(redis_obj,tag_id):
	''' Function which return the bookmark ids for tag id '''

	key = "tagId:%d:bookmarkIds" %(tag_id)
	return redis_obj.members_in_set(key)