# Create your views here.
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django import forms

from redis_helpers.views import Redis
from tags.forms import TagForm
from bookmark.bookmarks import get_bookmarks
from auth.login_status import is_logged_in
from auth.signin import login

from tags.getters import *
from tags.setters import *
from tags.deleters import *

def tag_name_exists(redis_obj,name):
	''' Check if the tag name already exists '''

	key = "name:%s:tagId" % (name)
	return redis_obj.check_existence(key)

def create_tag(redis_obj,name):
	''' create a tag if exists and return the tag id
	else return the tag id of existing one '''

	if tag_name_exists(redis_obj,name) == 1 :
		key = "name:%s:tagId" % (name)
		return redis_obj.get_value(key)

	tag_id = get_next_tagId(redis_obj)
	store_tag_name(redis_obj,tag_id,name)
	store_tagId_name_mapping(redis_obj,tag_id,name)
	return tag_id

def store_tag_info(tag_form):
	''' store the tag information '''

	redis_obj = Redis()
	tag_id = create_tag(redis_obj,tag_form['name'])	
	bookmark_list = tag_form['bookmark_list']
	for bookmark in bookmark_list:
		add_bookmark_to_tag(redis_obj,tag_id,bookmark)

def tag_bundle(request):
	''' create a tag if it doesnt exist.Add urls to the
	existing ones '''

	email = request.COOKIES.get("email","")
	auth_token = request.COOKIES.get("auth","")

	if not is_logged_in(email,auth_token):
		return login(request)

	if request.method == "POST":
		tag_form = TagForm(data=request.POST)
		
		if tag_form.is_valid():

			tag_form_cleaned = tag_form.cleaned_data
			tag_form_cleaned['bookmark_list']  = request.POST.getlist('bookmark_list')
			store_tag_info(tag_form_cleaned)

			return HttpResponseRedirect('/success/')

		userId , data = get_bookmarks(request)
		bookmark_list = get_bookmark_list(data)
		tag_form.fields['bookmark_list'] = forms.MultipleChoiceField(choices=bookmark_list)
		return render_to_response('tags.html',{'tag_form':tag_form},context_instance=RequestContext(request))	

	userId , data = get_bookmarks(request)
	bookmark_list = get_bookmark_list(data)
	tag_form = TagForm()
	tag_form.fields['bookmark_list'] = forms.MultipleChoiceField(choices=bookmark_list)
	
	return render_to_response('tags.html',{'tag_form':tag_form},context_instance=RequestContext(request))	




