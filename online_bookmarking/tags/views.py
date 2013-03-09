# Create your views here.
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.http import Http404,HttpResponse
from django import forms

from redis_helpers.views import Redis
from tags.forms import TagForm
from bookmark.bookmarks import get_bookmarks
from auth.login_status import is_logged_in
from auth.signin import login, authentication

from tags.getters import *
from tags.setters import *
from tags.deleters import *

from bookmark.getters import *

import simplejson

from online_bookmarking.settings import CREATE_TAG_TEMPLATE_PATH
from online_bookmarking.settings import TAG_NAMES_LIST_TEMPLATE_PATH
from online_bookmarking.settings import BOOKMARKS_FOR_TAGS_TEMPLATE_PATH

def tag_name_exists(redis_obj, name):
	''' Check if the tag name already exists '''

	key = "name:%s:tagId" % (name)
	return redis_obj.check_existence(key)

def create_tag(redis_obj, name):
	''' create a tag if exists and return the tag id
	else return the tag id of existing one '''

	if tag_name_exists(redis_obj, name) == 1 :
		key = "name:%s:tagId" % (name)
		return redis_obj.get_value(key)

	tag_id = get_next_tagId(redis_obj)
	store_global_tagIds(redis_obj, tag_id)
	store_tag_name(redis_obj, tag_id, name)
	store_tagId_name_mapping(redis_obj, tag_id, name)
	return tag_id

def store_tag_info(tag_form):
	''' store the tag information '''

	redis_obj = Redis()
	tag_id = create_tag(redis_obj, tag_form['name'])	
	
	bookmark_list = tag_form['bookmark_ids']
	for bookmark in bookmark_list:
		add_bookmark_to_tag(redis_obj, tag_id, bookmark)
	
	tag_form['status'] = 'success'
	return simplejson.dumps(tag_form)

def get_tag_names(redis_obj):
	''' Returns a dictionary of tag info '''

	key = "global:tags:tagId"
	tag_ids = redis_obj.members_in_set(key)

	tag_info = [{} for i in xrange(len(tag_ids))]

	for i, tag_id in enumerate(tag_ids):
		tag_dict = {}
		tag_id = int(tag_id)
		tag_dict['tag_id'] = tag_id
		tag_dict['name'] = get_tag_name(redis_obj, tag_id)
		tag_info[i] = tag_dict

	return tag_info

@authentication('/tag')
def tag_bundle(request):
	''' create a tag if it doesnt exist.Add urls to the
	existing ones '''


	if request.method == "POST":

		if request.is_ajax():
			data = simplejson.loads(request.POST.keys()[0])
		else:
			data = request.POST

		tag_form = TagForm(data=data)
		name = data.get('name','')
		if tag_form.is_valid() and data.get('bookmark_ids','') != '' and data['bookmark_ids'] != '':
			tag_form_cleaned = tag_form.cleaned_data
			tag_form_cleaned['bookmark_ids'] = data['bookmark_ids']
			tag_json = store_tag_info(tag_form_cleaned)
			
			return HttpResponse(tag_json,mimetype='application/json')
	
		tag_form = {}
		tag_form['name'] = name
		tag_form['status'] = 'failure'
		tag_form['error'] = 'Invalid entries'
		return HttpResponse(simplejson.dumps(tag_form),mimetype='application/json')
	
	raise Http404()

@authentication('/tag_names')
def retrieve_tags(request):
	''' Retrieve all the tag names '''

	redis_obj = Redis()
	tag_info = get_tag_names(redis_obj)
	return render_to_response(TAG_NAMES_LIST_TEMPLATE_PATH,
		{
			'tag_info':tag_info
		},
		context_instance=RequestContext(request))

def get_bookmarks_for_tags(request, tag_id):
	''' Retrieve the bookmarks corresponding to the tag id '''

	email = request.COOKIES.get("email", "")
	auth_token = request.COOKIES.get("auth", "")

	if not is_logged_in(email, auth_token):
		redirect_uri = '/tags/' + tag_id
		return login(request, redirect_uri=redirect_uri)

	redis_obj = Redis()
	bookmark_ids = bookmark_for_tags(redis_obj, int(tag_id))

	bookmark_list = [{} for i in xrange(len(bookmark_ids))]

	for i, bookmark_id in enumerate(bookmark_ids):
		bookmark_info = {}
		bookmark_id = int(bookmark_id)
		bookmark_info['url'] = get_url(redis_obj, bookmark_id)
		bookmark_info['name'] = get_name(redis_obj, bookmark_id)
		bookmark_info['description'] = get_description(redis_obj, bookmark_id)

		bookmark_list[i] = bookmark_info

	return render_to_response(BOOKMARKS_FOR_TAGS_TEMPLATE_PATH,
		{
			'bookmark_list':bookmark_list
		},
		context_instance=RequestContext(request))

	return Http404()




