from redis_helpers.views import Redis

def store_tag_name(redis_obj,tag_id,name):
	''' store the name of the tag '''

	key = "tagId:%d:name" % (tag_id)
	redis_obj.set_value(key,name)

def store_tagId_name_mapping(redis_obj,tag_id,name):
	''' reverse mapping of tag name with tag id '''

	key = "name:%s:tagId" % (name)
	redis_obj.set_value(key,tag_id)

def add_bookmark_to_tag(redis_obj,tag_id,bookmark_id):
	''' add the bookmark to the set in tag ids '''

	key = "tagId:%d:bookmarkIds" % (tag_id)
	redis_obj.add_to_set(key,bookmark_id)
