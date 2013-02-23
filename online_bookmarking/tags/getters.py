from redis_helpers.views import Redis

def get_next_tagId(redis_obj):
	''' Get the next unique tag id '''
	
	key = "global:tagId"
	return redis_obj.next_unique_key(key)

def get_bookmark_list(data):
	''' Function which returns id value format of bookmarks
	suitable for multi select dropdown '''

	return tuple([(i['bookmark_id'],i['name']) for i in data])