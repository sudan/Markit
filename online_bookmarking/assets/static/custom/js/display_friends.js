(function($,window,document,undefined){

	"use strict"

	var displayFriend = Backbone.Model.extend({
		defaults:{
			image_url:'',
			name:'',
			relationship_status:'',
			following_count:'',
			followers_count:'',
			others_id: ''
		}
	});

	var displayFriends = Backbone.Collection.extend({
		model: displayFriend
	});

	var userInfoView = Backbone.View.extend({
		el: $('#user_info'),

		initialize: function()
		{

		},

		events:
		{
			'click .followers':'getFriends',
			'click .following':'getFriends'
		},

		getFriends: function(e)
		{
			e.preventDefault();
			var anchor = e.currentTarget;
			var relationType = $(anchor).attr('class');
			var username = this.$el.find('b.title').text();
		
			this.displayFriends = new displayFriendsView(relationType,username);
		}
	});

	var displayFriendView = Backbone.View.extend({
		
		tagName: 'table',
		template: $('#friendsList').html(),
		render: function()
		{
			var tmpl = _.template(this.template);
			this.$el.html(tmpl(this.model.toJSON()));
			return this;
		}
	});

	var displayFriendsView = Backbone.View.extend({

		el:$('#follower_following_wrapper'),
		initialize: function(relationType,username)
		{
			this.relationType = relationType;
			this.username = username;
			this.friendsListWrapper =  $('#friends_list_wrapper')
			this.fetchFriends();
			
		},

		events:
		{
			'click .unfollow':'toggle',
			'click .follow':'toggle',
			'click button.close':'closeFriendsList',
		},

		closeFriendsList: function()
		{
			this.$el.slideUp(700);
		},

		toggle: function(e)
		{
			
			e.preventDefault();
			var self = this;
			
			var relationShipRequest = e.currentTarget.value;
			var othersId = $(e.currentTarget).prev().val();

			var toggle = new ToggleRelationShip({
				others_id: othersId,
				relationship_request: relationShipRequest
			});
			
			$.loadImage();

			toggle.save({
				success: function(response)
				{

				},
				error: function(response)
				{

				}
			}).complete(function(response){
				$.hideImage();
				var response = JSON.parse(response.responseText);
				if(response['status'])
				{
					
					if(response['toggle_status'] == 'follow')
					{
						$(e.currentTarget)
							.removeClass('btn-primary')
							.addClass('btn')
							.val('follow')
					}
					else if(response['toggle_status'] == 'unfollow')
					{
						$(e.currentTarget)
							.removeClass('btn')
							.addClass('btn-primary')
							.val('unfollow');
					}
				}
			});
		},

		fetchFriends: function()
		{
			var self = this;

			self.collection = new displayFriends();
			if(self.relationType == "following")
				self.collection.url = "/relation/following/" + self.username;
			else
				self.collection.url = "/relation/followers/" + self.username;

			self.collection.fetch({
				success: function()
				{

				},
				error: function()
				{

				}
			}).complete(function(response){
				var response = JSON.parse(response.responseText);
				self.render(response);
			});
		},

		render: function(friends)
		{
			var self = this;
			self.$el.find(self.friendsListWrapper).empty();
			_.each(friends,function(friend){
				self.renderFriend(friend);
			});

			self.$el.hide().slideDown(700);
		},

		renderFriend: function(friend)
		{
			var friend = new displayFriend({
				image_url: friend['image_url'],
				username: friend['username'],
				relationship_status: friend['relationship_status'],
				following_count: friend['following_count'],
				followers_count: friend['followers_count'],
				others_id: friend['others_id']
			});

			var friendView = new displayFriendView({
				model: friend
			});

			this.$el.find(this.friendsListWrapper).append(friendView.render().el);
		}

	});

	window.userInfo = new userInfoView();

})(jQuery,window,document);