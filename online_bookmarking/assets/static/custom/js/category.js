(function($,window,document,undefined){

	"use strict"

	var Category = Backbone.Model.extend({
		defaults:{
			name: '',
			category_id: ''
		},
		urlRoot: '/category/'
	});

	var CategoryView = Backbone.View.extend({
		
		el:$('#category_list'),

		initialize: function()
		{
			var self = this;

			self.createCategoryFormDiv = $('#create_category');
			self.categoryNameErrorSpan = $('#category_name_error');	
		},

		events:
		{
			"click #display_category_form_button":"showHideCategoryForm",
			"click #add_category":"saveCategory",
		},

		showHideCategoryForm: function()
		{
			var self = this;

			self.$el.find(self.createCategoryFormDiv).slideToggle();

			self.createCategoryFormDiv.find('input[name=name]').val('');
			self.categoryNameErrorSpan.empty();

		},

		saveCategory: function(e)
		{
			var self = this;
			e.preventDefault();
			
			var category_form_data = {};
			category_form_data["name"] = self.createCategoryFormDiv.find('input[name=name]').val();

			var category = new Category(category_form_data);
			$.loadImage();

			category.save({
				
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
					self.showHideCategoryForm();
			});			

		},

		displayErrorMessages: function(responseText)
		{
			window.self = this;

			if(responseText['name'])
				self.createCategoryFormDiv
					.find(self.categoryNameErrorSpan)
					.text(responseText['name']);
		}
	
	});

	window.category = new CategoryView();

})(jQuery,window,document)