(function($,window,document,undefined){

	"use strict"

	var Tag = Backbone.Model.extend({
		defaults:{
			name: '',
			tag_id: '',
			bookmark_id: '',
		},
		urlRoot: '/tag/'
	});

	var TagView = Backbone.View.extend({
		
		el:$('#tag_list'),

		initialize: function()
		{
			var self = this;

			self.createTagFormDiv = $('#create_tag');
			self.TagNameErrorSpan = $('#tag_name_error');	
		},

		events:
		{
			"click #display_tag_form_button":"showHideTagForm",
			"click #add_tag":"saveTag",
		},

		showHideTagForm: function(e)
		{
			var self = this;
			e.preventDefault();

			self.$el.find(self.createTagFormDiv).slideToggle();

			self.createTagFormDiv.find('input[name=name]').val('');
			self.TagNameErrorSpan.empty();

		},

		saveTag: function(e)
		{
			var self = this;
			e.preventDefault();
			
			var tag_form_data = {};
			tag_form_data["name"] = self.createTagFormDiv.find('input[name=name]').val();

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
			window.self = this;

			if(responseText['name'])
				self.createTagFormDiv
					.find(self.TagNameErrorSpan)
					.text(responseText['name']);
		}
	
	});

	window.tag = new TagView();

})(jQuery,window,document)