(function($,window,document,undefined){

	$.getCookie = function(name) 
	{
    	var cookieValue = null;
    	if (document.cookie && document.cookie != '') 
    	{
        	var cookies = document.cookie.split(';');
        	for (var i = 0; i < cookies.length; i++) 
        	{
            	var cookie = jQuery.trim(cookies[i]);
            	
            	if (cookie.substring(0, name.length + 1) == (name + '=')) 
            	{
                	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                	break;
            	}
        	}
    	}
    	return cookieValue;
	};

    $.loadImage = function()
    {
        $('#image-loader').fadeIn();
    };

    $.hideImage = function()
    {
        $('#image-loader').fadeOut();
    };

    $.refreshBookmarks = function()
    {
        var tagAnchor = $('#display_tag_form_button');
        var tagForm = $('#create_tag');
        if(tagForm.is(":visible"))
            tagForm.slideUp();
    };

    $.showSuccess = function()
    {
        var message = $('.alert');
        message.fadeIn();
    };

    $.hideSuccess = function()
    {
        var message = $('.alert');
        message.fadeOut();
    };

})(jQuery,window,document);