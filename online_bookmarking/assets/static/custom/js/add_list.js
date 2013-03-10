(function($,window,document,undefined){

	"use strict"
	
	var addListBookmark = Backbone.Model.extend({
		defaults:{
			url: '',
			name: '',
			description: '',
			visibility: ''
		},
		urlRoot: '/bookmark/'
	});

	var addListBookmarkView = Backbone.View.extend({
		el: $('#bookmarks_wrapper'),

		initialize: function()
		{
			
		},

		events: {
			'click img.add_bookmark_icon': 'addBookmarkToMyList'
		},

		addBookmarkToMyList: function(e)
		{
			$.loadImage();
			$.hideSuccess();
			
			var img = $(e.currentTarget);
			var url = img.closest('li').find('a').attr('href');
			var name = img.closest('li').find('a').text();
			var description = img.closest('li').children('p.description').text();

			var addBookmark = new addListBookmark({
				url: url,
				name: name,
				description: description,
				visibility: 'public'
			});

			addBookmark.save().complete(function(){
				$.hideImage();
				$.showSuccess();
			});


		}


	});

	window.add_list_bookmark = new addListBookmarkView();

})(jQuery,window,document);