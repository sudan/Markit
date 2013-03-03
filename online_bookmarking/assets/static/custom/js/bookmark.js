(function($,window,document,undefined){

	var Bookmark = Backbone.Model.extend({
		defaults:{
			url: '',
			name: '',
			description: '',
			visibility: '',
			created_date: '',
			bookmark_id: ''
		},
		urlRoot: '/bookmark'
	});

	var Bookmarks = Backbone.Collection.extend({
		model: Bookmark,
		url: '/bookmarks'
	});

})(jQuery,window,document);