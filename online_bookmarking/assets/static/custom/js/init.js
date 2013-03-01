(function($,window,document,undefined){

	var layoutSettings =
	{
	    Name    :   "Main",
	    Dock    :   $.layoutEngine.DOCK.FILL,
	    EleID   :   "main",       
	    Children:
	    [
	        {
	            Name    :   "Top",
	            Dock    :   $.layoutEngine.DOCK.TOP,
	            EleID   :   "top",                           
	            Height  :   75
	        },
	        {
                Name    :   "Left",
                Dock    :   $.layoutEngine.DOCK.LEFT,
                EleID   :   "left",
                Width   :   300
            },
            {
                Name    :   "Fill",
                Dock    :   $.layoutEngine.DOCK.FILL,
                EleID   :   "fill"
            },
	        {
	            Name    :   "Right",
	            Dock    :   $.layoutEngine.DOCK.RIGHT,
	            EleID   :   "right",                          
	           	Width   :   420,
	           	Height  :   500
	                        
	        },                        
	       	{
	            Name    :   "Bottom",
	            Dock    :   $.layoutEngine.DOCK.BOTTOM,
	            EleID   :   "bottom",
	            Height  :   50
	        }
	    ]
	             
	};

	$.layoutEngine(layoutSettings);


})(jQuery,window,document);