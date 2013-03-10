(function($,window,document,undefined){

	"use strict"

	var BookmarkCategory = Backbone.Model.extend({
		defaults:{
			category_id: '',
			bookmark_ids: ''
		},
		urlRoot:'/add_bookmarks_to_category/'
	});

	var BookmarkCategoryView = Backbone.View.extend({

		el:$('#bookmark_category_list'),

		initialize: function()
		{
			this.bookmarkCategoryFormDiv = $('#bookmark_category_wrapper');
			this.categoryDropDownWrapper = $('.category_dropdown');
			this.bookmarkDropDownWrapper = $('.bookmark_dropdown');
			this.categoryDropDown = 'bookmark_dropdown_list';
			this.bookmarkDropDown = 'category_dropdown_list';
			this.bookmarkCategoryErrorSpan = $('#bookmark_category_error');
		},

		events:
		{
			'click #display_bookmark_category_button':'showHideBookmarkCategoryForm',
			'click #add_bookmarks_to_category':'saveBookmarkCategoryMapping',
		},

		showHideBookmarkCategoryForm: function(e)
		{
			this.buildCategoryDropDown();
			this.buildBookmarkDropDown();
			this.bookmarkCategoryFormDiv.slideToggle();
			this.bookmarkCategoryErrorSpan.empty();
		},

		buildCategoryDropDown: function()
		{
			var self = this;
			var select = $('<select/>',{
				id: self.categoryDropDown
			});

			self.categoryDropDownWrapper.empty();
			_.each(categories.collection.models,function(model){
				var option = $('<option/>',{
					text: model.get('name'),
					value: model.get('category_id')
				}).appendTo(select);
			});

			select.appendTo(self.categoryDropDownWrapper)
			select.chosen();
			return select;
		},

		buildBookmarkDropDown: function()
		{
			var self = this;
			self.bookmarkDropDownWrapper.empty();

			var select = $('<select/>',{
				id:self.bookmarkDropDown,
				multiple: true,
				'data-placeholder': 'Select bookmarks'
			});

			_.each(bookmarks.collection.models,function(model){

				var option = $('<option/>',{
					text: model.get("name"),
					value: model.get("bookmark_id")
				}).appendTo(select);

			});
			select.appendTo(self.bookmarkDropDownWrapper);
			select.chosen();
			return select;
		},

		saveBookmarkCategoryMapping: function(e)
		{
			e.preventDefault();

			var self = this;
			var categoryId = $('#' + self.categoryDropDown).val();
			var bookmarkIds = $('#' + self.bookmarkDropDown).val();
			
			var bookmark_category = new BookmarkCategory({
				category_id: categoryId,
				bookmark_ids: bookmarkIds
			});

			$.loadImage();
			bookmark_category.save({

				success: function(response)
				{

				},
				error: function(response)
				{

				}

			}).complete(function(response){
				$.hideImage();
				var responseText = JSON.parse(response.responseText);

				if(responseText['status'] == 'success')
				{
					self.showHideBookmarkCategoryForm();
					self.updateCategoryIds(responseText);
				}
				else
				{
					self.displayErrorMessages(responseText);
				}
			});

		},

		displayErrorMessages: function(responseText)
		{
			if(responseText['category_id'] || responseText['bookmark_ids'])
				self.bookmarkCategoryErrorSpan.text('Invalid entries');
		},

		updateCategoryIds: function(responseText)
		{

			var cidBookmarkIdMapping = {}
			bookmarks.collection.each(function(model){
				cidBookmarkIdMapping[model.get('bookmark_id')] = model.cid;
			});
			
			var bookmarkIds = responseText['bookmark_ids'];
			var categoryId = responseText['category_id'];
			
			$.each(bookmarkIds,function(index,bookmarkId){
				
				var cid = cidBookmarkIdMapping[bookmarkId];
				var model = bookmarks.collection.getByCid(cid);
				model.set({'category_id':categoryId});
			});

		},

	});

	window.bookmark_category = new BookmarkCategoryView();

})(jQuery,window,document);