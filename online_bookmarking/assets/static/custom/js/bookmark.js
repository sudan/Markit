(function($,window,document,undefined){

	"use strict"
	
	var Bookmark = Backbone.Model.extend({
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

	var Bookmarks = Backbone.Collection.extend({
		model: Bookmark,
		url: '/bookmarks/'
	});

	var BookmarkView = Backbone.View.extend({
		tagName: 'div',
		className: 'bookmark',
		template: $('#bookmarkDisplayTemplate').html(),
		editTemplate: $('#bookmarkEditTemplate').html(),
		
		render: function()
		{			
			var tmpl = _.template(this.template);
			this.$el.html(tmpl(this.model.toJSON()));
			return this;
		},

		events:
		{	
			'click button.edit_bookmark':'editBookmark',
			'click button.cancel_bookmark':'cancelBookmark',
			'click button.save_bookmark':'saveBookmark',
			'click button.delete_bookmark':'deleteBookmark',
		},

		editBookmark: function()
		{	
			var tmpl = _.template(this.editTemplate);
			this.$el.html(tmpl(this.model.toJSON())).hide().slideDown();
		},

		deleteBookmark: function()
		{
			var self = this;
			var bookmark_id = this.model.get("bookmark_id");
			
			$.ajax({
				type: 'POST',
				data: {'bookmark_id':bookmark_id},
				url: '/delete_bookmark/',
				headers: { "X-CSRFToken": $.getCookie("csrftoken") },
				success: function()
				{
					self.model.destroy();
					self.remove();
				},
				error: function(error)
				{
					console.log(error)
				}
			});

			
		},

		cancelBookmark: function(e)
		{	
			e.preventDefault();
			this.render();
		},

		displayErrorMessages: function(editBookmarkForm,responseText)
		{
			var responseText = responseText;
			var self = this;
			
			if(responseText['url'] || responseText['name'] || responseText['visibility'] || responseText['description'])
				editBookmarkForm
					.find($('.edit_bookmark_error_messages'))
					.text('Invalid entries');
		},

		saveBookmark: function(e)
		{	
			var self = this;
			e.preventDefault();
			var prevModel = this.model.previousAttributes();

			var bookmark_form_data = {}
			var editBookmarkForm = $('#edit_bookmark_form');

			bookmark_form_data['url'] = editBookmarkForm.find('input[name=url]').val();
			bookmark_form_data['name'] = editBookmarkForm.find('input[name=name]').val();
			bookmark_form_data['description'] = editBookmarkForm.find('input[name=description]').val();
			if(editBookmarkForm.find('input[value=public]').is(':checked'))
				bookmark_form_data['visibility'] = 'public';
			else
				bookmark_form_data['visibility'] = 'private';			
			bookmark_form_data['bookmark_id'] = editBookmarkForm.find('input[name=bookmark_id]').val();
			
			var bookmark = new Bookmark(bookmark_form_data);
			
			$.loadImage();
			var response = bookmark.save({

			 	success: function(response)
			 	{
			 		
				},
				error: function(error)
				{
			 		
				}
			}).complete(function(response){

				$.hideImage();
				$.refreshBookmarks();
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

	var BookmarksView = Backbone.View.extend({
		el: $('#bookmark_list'),

		initialize: function()
		{
			
			var self = this;
			this.createBookmarkDiv = $('#create_bookmark');
			this.createBookmarkFormDiv = $('#add_bookmark_form');
			this.bookmarkWrapperDiv = $('#bookmark_wrapper');
			this.bookmarkUrlErrorSpan = $('.bookmark_url_error');
			this.bookmarkNameErrorSpan = $('.bookmark_name_error');
			this.bookmarkDescriptionErrorSpan = $('.bookmark_description_error');
			this.bookmarkVisibilityErrorSpan = $('.bookmark_visibility_error');

			this.collection = new Bookmarks();
			$.loadImage();
			this.collection.fetch({

				success: function(response)
				{
					$.hideImage();
					self.render();
				},
				error: function(error)
				{

				}
			});

			this.collection.on("add",this.renderBookmark,this);
		
		},

		render: function()
		{
			var self = this;
			_.each(this.collection.models,function(bookmark){
				self.renderBookmark(bookmark);
			},this);
		},

		renderBookmark: function(bookmark)
		{
			var bookmarkView = new BookmarkView({
				model: bookmark
			});

			if(bookmark.get('status') == 'success')
			{
				this.$el.find(this.bookmarkWrapperDiv)
					.prepend(bookmarkView.render().el)
					.hide()
					.slideDown();
				this.showHideBookmarkForm();
			}	
			else
				this.$el.find(this.bookmarkWrapperDiv)
					.append(bookmarkView.render().el);

		},

		events:
		{
			"click #display_bookmark_form_button": "showHideBookmarkForm",
			"click #add_bookmark": "addBookmark",
		},

		showHideBookmarkForm: function()
		{
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

		displayErrorMessages: function(responseText)
		{
			var self = this;

			if(responseText['url'])
				self.createBookmarkFormDiv
					.find(self.bookmarkUrlErrorSpan)
					.text(responseText['url']);
			
			if(responseText['name'])
				self.createBookmarkFormDiv
					.find(self.bookmarkNameErrorSpan)
					.text(responseText['name']);
			
			if(responseText['description'])
				self.createBookmarkFormDiv
					.find(self.bookmarkDescriptionErrorSpan)
					.text(responseText['description']);
			
			if(responseText['visibility'])
				self.createBookmarkFormDiv
					.find(self.bookmarkVisibilityErrorSpan)
					.text(responseText['visibility']);
		},

		addBookmark: function(e)
		{
			var self = this;
			e.preventDefault();
			
			var bookmark_form_data = {};
			
			bookmark_form_data['url'] = this.createBookmarkFormDiv.find('input[name=url]').val();
			bookmark_form_data['name'] = this.createBookmarkFormDiv.find('input[name=name]').val();
			bookmark_form_data['description'] = this.createBookmarkFormDiv.find('textarea[name=description]').val();
			if(this.createBookmarkFormDiv.find('input[value=public]').is(':checked'))
				bookmark_form_data['visibility'] = 'public';
			else
				bookmark_form_data['visibility'] = 'private';			
			
			var bookmark = new Bookmark(bookmark_form_data);
			
			$.loadImage();
			bookmark.save({
				
				success: function(response)
				{
					
				},
				error: function(error)
				{
				
				}
			
			}).complete(function(response){

				$.hideImage();
				$.refreshBookmarks();
				var responseText = JSON.parse(response.responseText);
				if(responseText.status == "success")
					self.collection.add(new Bookmark(responseText));
				else
					self.displayErrorMessages(responseText);	
			});			
		},

	});
	     
    Backbone._sync = Backbone.sync;

    Backbone.sync = function(method, model, options) 
    {

    	if (method == 'create' || method == 'update' || method == 'delete')
    	{
        	options.beforeSend = function(xhr)
        	{
            	xhr.setRequestHeader('X-CSRFToken', $.getCookie('csrftoken'));
            	xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
           	};
        }
        return Backbone._sync(method, model, options);
    
    };

	window.bookmarks = new BookmarksView();

})(jQuery,window,document)