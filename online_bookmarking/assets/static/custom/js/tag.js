(function($,window,document,undefined){

	"use strict"

	window.Tag = Backbone.Model.extend({
		defaults:{
			name: '',
			tag_id: '',
			bookmark_ids: '',
		},
		urlRoot: '/tag/'
	});

	var TagView = Backbone.View.extend({
		
		el:$('#tag_list'),

		initialize: function()
		{
			var self = this;

			self.createTagFormDiv = $('#create_tag');
			self.tagNameErrorSpan = $('#tag_name_error');	
			self.bookmarkDropDownId = 'bookmark_dropdown';
		},

		events:
		{
			"click #display_tag_form_button":"showHideTagForm",
			"click #add_tag":"saveTag",
		},

		showHideTagForm: function()
		{
			var self = this;
			self.$el.find('#bookmark_tag_wrapper')
				.empty()
				.append(self.createBookmarkDropDown());
			
			$('#' + self.bookmarkDropDownId).chosen()
			$('#' + self.bookmarkDropDownId).trigger("liszt:updated");

			self.$el.find(self.createTagFormDiv).slideToggle();

			self.createTagFormDiv.find('input[name=name]').val('');
			self.tagNameErrorSpan.empty();

		},

		saveTag: function(e)
		{
			var self = this;
			e.preventDefault();
			
			var tag_form_data = {};
			tag_form_data["name"] = self.createTagFormDiv.find('input[name=name]').val();
			tag_form_data["bookmark_ids"] = self.createTagFormDiv
												.find($('#bookmark_dropdown')).val();
			var tag = new Tag(tag_form_data);
			$.loadImage();
			
			tag.save({
				
				success: function(response)
				{
					
				},
				error: function(error)
				{
				
				}
			
			}).complete(function(response){

				$.hideImage();
				var responseText = JSON.parse(response.responseText);
				
				if(responseText.status == "failure")
					self.displayErrorMessages(responseText);
				else
					self.showHideTagForm();
			});			

		},

		displayErrorMessages: function(responseText)
		{
			var self = this;
			
			if(responseText['error'])
				self.createTagFormDiv
					.find(self.tagNameErrorSpan)
					.text(responseText['error']);
		},

		createBookmarkDropDown: function()
		{
			var self = this;

			var select = $('<select/>',{
				id: self.bookmarkDropDownId,
				multiple: true,
				'data-placeholder': 'Select bookmarks'
			});

			_.each(bookmarks.collection.models,function(model){

				var option = $('<option/>',{
					text: model.get("name"),
					value: model.get("bookmark_id")
				}).appendTo(select);

			});
			return select;
		}
	
	});

	window.tag = new TagView();

})(jQuery,window,document)