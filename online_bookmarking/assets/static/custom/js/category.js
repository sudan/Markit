(function($,window,document,undefined){

	"use strict"

	window.Category = Backbone.Model.extend({
		defaults:{
			name: '',
			category_id: ''
		},
		urlRoot: '/category/'
	});

	var Categories = Backbone.Collection.extend({
		model: Category,
		url:'/categories/'

	});

	var CategoriesView = Backbone.View.extend({
		el:$('#category_list'),

		initialize: function()
		{

			var self = this;

			self.createCategoryFormDiv = $('#create_category');
			self.categoryNameErrorSpan = $('#category_name_error');	
			self.categoriesDiv = $('#display_category');

			this.collection = new Categories();
			
			this.collection.fetch({
				
				success: function(response)
				{
					$.loadImage();
					self.render();
					$.hideImage();		
				},
				error: function(response)
				{

				}

			});

			this.collection.on("add",this.render,this);
			this.on("change:filterType", this.filterBookmarks, this);
		},

		events:
		{
			"click #display_category_form_button": "showHideCategoryForm",
			"click #add_category": "saveCategory",
			"change #display_category select": "setFilter",
		},

		setFilter: function(e)
		{
			this.filterType = e.currentTarget.value;
			this.trigger("change:filterType");
		},

		filterBookmarks: function()
		{

			if(this.filterType == "All")
			 	bookmarks.collection.reset(bookmarks.bookmarks_json);
			else
			{
			 	bookmarks.collection.reset(bookmarks.bookmarks_json,{silent:true});
			 	var filterType = this.filterType;
			 	var filtered = _.filter(bookmarks.collection.models,function(model){
			 		return model.get('category_id') == filterType;
			 	});
			 	bookmarks.collection.reset(filtered);
			}
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
				{	
					self.showHideCategoryForm();
					if(responseText.status != "duplicate")
						self.collection.add(category);

				}
			});			

		},

		displayErrorMessages: function(responseText)
		{
			var self = this;

			if(responseText['name'])
				self.createCategoryFormDiv
					.find(self.categoryNameErrorSpan)
					.text(responseText['name']);
		},

		render: function()
		{

			this.categoriesDiv.empty();

			var select = $('<select/>',{
				id: 'categories',
				'data-placeholder':'Select a category'
			});

			var option = $('<option/>',{
				value: 'All',
				text: 'All'
			}).appendTo(select);

			_.each(this.collection.models,function(model){
				var option = $('<option/>',{
					
					text: model.get("name"),
					value: model.get("category_id")

				}).appendTo(select);

			});

			select.appendTo(this.categoriesDiv);
			select.chosen();

			this.categoriesDiv.show();
		}

	});
	
	window.categories = new CategoriesView();

})(jQuery,window,document)