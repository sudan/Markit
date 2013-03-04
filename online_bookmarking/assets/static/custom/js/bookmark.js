(function($,window,document,undefined){

	"use strict"
	
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

	window.Bookmarks = Backbone.Collection.extend({
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
			this.bookmarkWrapperDiv = $('#bookmark_wrapper');

			this.collection = new Bookmarks();
			this.collection.fetch({

				success: function(){
					self.render();
				},
				error: function(){

				}

			});

			this.collection.on("add",this.renderBookmark,this);
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

			if(bookmark.get('status') == 'success')
			{
				this.$el.find("#bookmark_wrapper").prepend(bookmarkView.render().el).hide().slideDown();
				this.showHideBookmarkForm();
			}	
			else
				this.$el.find("#bookmark_wrapper").append(bookmarkView.render().el);

		},

		events:{
			"click #display_bookmark_form_button": "showHideBookmarkForm",
			"click #add_bookmark": "addBookmark",
		},

		showHideBookmarkForm: function(){
			
			this.createBookmarkDiv.slideToggle(); 
			
			this.createBookmarkFormDiv.find('input[name=url]').val('');
			this.createBookmarkFormDiv.find('input[name=name]').val('');
			this.createBookmarkFormDiv.find('textarea[name=description]').val('');

			this.createBookmarkFormDiv.find(".bookmark_url_error").empty();
			this.createBookmarkFormDiv.find(".bookmark_name_error").empty();
			this.createBookmarkFormDiv.find(".bookmark_description_error").empty();
			this.createBookmarkFormDiv.find(".bookmark_visibility_error").empty();
		},

		displayErrorMessages: function(responseText){

			window.responseText = responseText;
			if(responseText['url'])
				this.createBookmarkFormDiv.find(".bookmark_url_error").text(responseText['url']);
			if(responseText['name'])
				this.createBookmarkFormDiv.find(".bookmark_name_error").text(responseText['name']);
			if(responseText['description'])
				this.createBookmarkFormDiv.find(".bookmark_description_error").text(responseText['description']);
			if(responseText['visibility'])
				this.createBookmarkFormDiv.find(".bookmark_visibility_error").text(responseText['visibility']);

		},

		addBookmark: function(e){
			
			e.preventDefault();
			var self = this;
			
			var bookmark_form_data = {};
			bookmark_form_data['url'] = this.createBookmarkFormDiv.find('input[name=url]').val();
			bookmark_form_data['name'] = this.createBookmarkFormDiv.find('input[name=name]').val();
			bookmark_form_data['description'] = this.createBookmarkFormDiv.find('textarea[name=description]').val();
			bookmark_form_data['visibility'] = this.createBookmarkFormDiv.find('input[name=visibility]').val();
			
			var bookmark = new Bookmark(bookmark_form_data);
			console.log(bookmark);

			bookmark.save({
				success: function(response){
					console.log(response)
				},
				error: function(error){
					console.log(error);
				}
			}).complete(function(response){
				window.responseText = JSON.parse(response.responseText);
				if(responseText.status == "success")
					self.collection.add(new Bookmark(responseText));
				else
					self.displayErrorMessages(responseText);
				
			});

			
		}

	});

	     
    Backbone._sync = Backbone.sync;

    Backbone.sync = function(method, model, options) {

    	if (method == 'create' || method == 'update' || method == 'delete') {

        	options.beforeSend = function(xhr){
            	    xhr.setRequestHeader('X-CSRFToken', $.getCookie('csrftoken'));
            	    xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
            	};
        	}
       window.options = options;
            
        return Backbone._sync(method, model, options);
    };

	var bookmarks = new BookmarksView();

})(jQuery,window,document)