(function($,window,document,undefined){

	"use strict"
	
	window.Bookmark = Backbone.Model.extend({
		defaults:{
			url: '',
			name: '',
			description: '',
			visibility: '',
			creation_date: '',
			bookmark_id: ''
		},

		urlRoot: '/bookmark/'
	});

	window.Bookmarks = Backbone.Collection.extend({
		model: Bookmark,
		url: '/bookmarks/'
	});

	var BookmarkView = Backbone.View.extend({
		tagName: 'div',
		className: 'bookmark',
		template: $('#bookmarkDisplayTemplate').html(),
		editTemplate: $('#bookmarkEditTemplate').html(),
		
		render: function(){
			
			var tmpl = _.template(this.template);
			this.$el.html(tmpl(this.model.toJSON()));
			return this;
		},

		events:{
			'click button.edit_bookmark':'editBookmark',
			'click button.cancel_bookmark':'cancelBookmark',
			'click button.save_bookmark':'saveBookmark',
		},

		editBookmark: function(){
			
			var tmpl = _.template(this.editTemplate);
			this.$el.html(tmpl(this.model.toJSON())).hide().slideDown();

		},

		cancelBookmark: function(e){
			
			e.preventDefault();
			this.render();
		},

		displayErrorMessages: function(editBookmarkForm,responseText){

			var responseText = responseText;
			var self = this;
			
			if(responseText['url'] || responseText['name'] || responseText['visibility'] || responseText['description'])
				editBookmarkForm.find($('.edit_bookmark_error_messages')).text('Invalid entries');

		},

		saveBookmark: function(e){
			
			var self = this;
			e.preventDefault();
			var prevModel = this.model.previousAttributes();

			var bookmark_form_data = {}
			var editBookmarkForm = $('#edit_bookmark_form');
			bookmark_form_data['url'] = editBookmarkForm.find('input[name=url]').val();
			bookmark_form_data['name'] = editBookmarkForm.find('input[name=name]').val();
			bookmark_form_data['description'] = editBookmarkForm.find('input[name=description]').val();
			bookmark_form_data['visibility'] = editBookmarkForm.find('input[name=visibility]').val();
			bookmark_form_data['bookmark_id'] = editBookmarkForm.find('input[name=bookmark_id]').val();
			
			var bookmark = new Bookmark(bookmark_form_data)
			
			var response = bookmark.save({
			 	success: function(response){
			 		console.log(response)
				},
			error: function(error){
			 		console.log(error);
				}
			}).complete(function(response){
				var responseText = JSON.parse(response.responseText);
				if(responseText.status == "failure")
					self.displayErrorMessages(editBookmarkForm,responseText);
				else
				{
					self.model.set(bookmark_form_data)
					self.render();
				}
			});	


		}

	});

	window.BookmarksView = Backbone.View.extend({
		el: $('#bookmark_list'),

		initialize: function(){
			
			var self = this;
			this.createBookmarkDiv = $('#create_bookmark');
			this.createBookmarkFormDiv = $('#add_bookmark_form');
			this.bookmarkWrapperDiv = $('#bookmark_wrapper');
			this.bookmarkUrlErrorSpan = $('.bookmark_url_error');
			this.bookmarkNameErrorSpan = $('.bookmark_name_error');
			this.bookmarkDescriptionErrorSpan = $('.bookmark_description_error');
			this.bookmarkVisibilityErrorSpan = $('.bookmark_visibility_error');

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
				this.$el.find(this.bookmarkWrapperDiv).prepend(bookmarkView.render().el).hide().slideDown();
				this.showHideBookmarkForm();
			}	
			else
				this.$el.find(this.bookmarkWrapperDiv).append(bookmarkView.render().el);

		},

		events:{
			"click #display_bookmark_form_button": "showHideBookmarkForm",
			"click #add_bookmark": "addBookmark",
		},

		showHideBookmarkForm: function(){
			
			var self = this;
			self.createBookmarkDiv.slideToggle(); 
			
			self.createBookmarkFormDiv.find('input[name=url]').val('');
			self.createBookmarkFormDiv.find('input[name=name]').val('');
			self.createBookmarkFormDiv.find('textarea[name=description]').val('');

			self.createBookmarkFormDiv.find(self.bookmarkUrlErrorSpan).empty();
			self.createBookmarkFormDiv.find(self.bookmarkNameErrorSpan).empty();
			self.createBookmarkFormDiv.find(self.bookmarkDescriptionErrorSpan).empty();
			self.createBookmarkFormDiv.find(self.bookmarkVisibilityErrorSpan).empty();
		},

		displayErrorMessages: function(responseText){

			var responseText = responseText;
			var self = this;

			if(responseText['url'])
				self.createBookmarkFormDiv.find(self.bookmarkUrlErrorSpan).text(responseText['url']);
			if(responseText['name'])
				self.createBookmarkFormDiv.find(self.bookmarkNameErrorSpan).text(responseText['name']);
			if(responseText['description'])
				self.createBookmarkFormDiv.find(self.bookmarkDescriptionErrorSpan).text(responseText['description']);
			if(responseText['visibility'])
				self.createBookmarkFormDiv.find(self.bookmarkVisibilityErrorSpan).text(responseText['visibility']);

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
			
			bookmark.save({
				success: function(response){
					console.log(response)
				},
				error: function(error){
					console.log(error);
				}
			}).complete(function(response){
				var responseText = JSON.parse(response.responseText);
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
            
        return Backbone._sync(method, model, options);
    };

	var bookmarks = new BookmarksView();

})(jQuery,window,document)