(function($,window,document,undefined){

	"use strict"

	var Bookmark = Backbone.Model.extend({
		defaults:{
			url: '',
			name: '',
			description: '',
			visibility: '',
			creation_date: ''
		},
		urlRoot: '/bookmark'
	});

	var Bookmarks = Backbone.Collection.extend({
		model: Bookmark,
		url: '/bookmarks'
	});

	var BookmarkView = Backbone.View.extend({
		tagName: 'article',
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
			this.collection = new Bookmarks();
			this.collection.fetch({

				success: function(){
					self.render();
				},
				error: function(){

				}

			});
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
			this.$el.append(bookmarkView.render().el);

		}
	});

	var bookmarks = new BookmarksView();

})(jQuery,window,document)