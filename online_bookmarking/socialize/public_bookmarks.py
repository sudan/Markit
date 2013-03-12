from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from auth.helpers import get_userId
from auth.getters import *
from auth.signin import authentication
from redis_helpers.views import Redis
from socialize.profile import get_public_bookmarks
from online_bookmarking.settings import RECOMMENDATIONS_LIST_TEMPLATE_PATH

@authentication('/recommendations')
def get_recommendations(request):
	''' Get public bookmarks for the user '''

	redis_obj = Redis()
	user_id = get_userId(request)
	username = get_username(redis_obj,user_id)

	key = "userId:%d:following" %(user_id)
	following_ids = redis_obj.members_in_set(key)

	recommendations = []
	for following_id in following_ids:
		recommendations.extend(get_public_bookmarks(redis_obj,int(following_id),limit=5))
		if len(recommendations) > 50:
			break

	return render_to_response(RECOMMENDATIONS_LIST_TEMPLATE_PATH,
		{
			'recommendations':recommendations,
			'username':username
		},
		context_instance=RequestContext(request))