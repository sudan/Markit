(function($,window,document,undefined){

	"use strict"

	window.ToggleRelationShip = Backbone.Model.extend({
		defaults:{
			others_id:'',
			relationship_request:''
		},
		urlRoot:'/toggle/'
	});

	var ToggleRelationShipView = Backbone.View.extend({
		el: $('.user_profile'),
		
		initialize: function()
		{
			
		},

		events:
		{
			'click .relationship_button':'toggleButton'
		},

		toggleButton: function(e)
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
					$(e.currentTarget)
						.closest('.users_list_wrapper')
						.find('.followers')
						.text(response['followers'] + " followers");

					$(e.currentTarget)
						.closest('.users_list_wrapper')
						.find('.following')
						.text(response['following'] + " following");
				}
			});
		}

	});

	window.toggleRelationShip = new ToggleRelationShipView();

})(jQuery,window,document);