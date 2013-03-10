from redis_helpers.views import Redis

def delete_bookmark_from_tag(redis_obj,bookmark_id):
	''' add the bookmark to the set in tag ids '''

	key = "global:tags:tagId"
	tag_ids = redis_obj.members_in_set(key)

	for tag_id in tag_ids:
		
		key = "tagId:%d:bookmarkIds" % (int(tag_id))
		redis_obj.remove_from_set(key, bookmark_id)