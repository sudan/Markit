(function($,window,document,undefined){

	"use strict"

	$.getCookie = function(name) 
	{
    	var cookieValue = null;
    	if (document.cookie && document.cookie != '') 
    	{
        	var cookies = document.cookie.split(';');
        	for (var i = 0; i < cookies.length; i++) 
        	{
            	var cookie = jQuery.trim(cookies[i]);
            	
            	if (cookie.substring(0, name.length + 1) == (name + '=')) 
            	{
                	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                	break;
            	}
        	}
    	}
    	return cookieValue;
	};
	
	window.Bookmark = Backbone.Model.extend({
		defaults:{
			url: '',
			name: '',
			description: '',
			visibility: '',
			creation_date: ''
		},

		urlRoot: '/bookmark/'
	});

	var Bookmarks = Backbone.Collection.extend({
		model: Bookmark,
		url: '/bookmarks'
	});

	var BookmarkView = Backbone.View.extend({
		tagName: 'div',
		className: 'bookmark',
		template: $('#bookmarkDisplayTemplate').html(),
		
		render: function(){
			
			var tmpl = _.template(this.template);
			this.$el.html(tmpl(this.model.toJSON()));
			return this;
		}
	});

	var BookmarksView = Backbone.View.extend({
		el: $('#bookmark_list'),

		initialize: function(){
			
			var self = this;
			this.createBookmarkDiv = $('#create_bookmark');
			this.createBookmarkFormDiv = $('#add_bookmark_form');

			this.collection = new Bookmarks();
			this.collection.fetch({

				success: function(){
					self.render();
				},
				error: function(){

				}

			});
		},

		render: function(){

			var self = this;
			_.each(this.collection.models,function(bookmark){
				self.renderBookmark(bookmark);
			},this);
		},

		renderBookmark: function(bookmark){

			var bookmarkView = new BookmarkView({
				model: bookmark
			});
			this.$el.append(bookmarkView.render().el);

		},

		events:{
			"click #display_bookmark_form_button": "displayBookmark",
			"click #add_bookmark": "addBookmark",
		},

		displayBookmark: function(){
			
			this.createBookmarkDiv.slideToggle();
		},

		addBookmark: function(e){
			e.preventDefault();
			
			var bookmark = new Bookmark	
		}

	});

	     
    Backbone._sync = Backbone.sync;

    Backbone.sync = function(method, model, options) {

    	if (method == 'create' || method == 'update' || method == 'delete') {

        	options.beforeSend = function(xhr){
            	    xhr.setRequestHeader('X-CSRFToken', $.getCookie('csrftoken'));
            	};
        	}

            
        return Backbone._sync(method, model, options);
    };

	var bookmarks = new BookmarksView();

})(jQuery,window,document)