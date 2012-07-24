define([
  "app",
  "backbone"
],

function(app, Backbone) {

  var Configuration = app.module();

  Configuration.Model = Backbone.Model.extend({
    url: function() {
        return "/configuration/";
    }
  });

  Configuration.View = Backbone.View.extend({
    template: "configuration/item",
    
    events: {
        "click .dim-save": "changeDimension",
        "click .start-mapping": "startMapping"
    },
    
    serialize: function() {
      return {
        model: this.model
      };
    },
    
    render: function(manage) {    	
    	return manage(this).render().then(function(el) {
    		var s = 50.0, w = this.model.get("w"), h = this.model.get("h"),
    		mapping = this.model.get("mapping"), label = '', tw = 0, th = 0,
    		fs = 20;
    		var canvas = document.getElementById("myCanvas");
    		canvas.width = w * s + 1;
    		canvas.height = h * s + 1;
            var context = canvas.getContext("2d");
            context.font = "normal " + fs + "px Sans";
            context.strokeStyle = "#ccc";
            
            for (var y = 0; y < h; y++){
            	for (var x = 0; x < w; x++){
            		context.rect(x * s + 0.5, y * s + 0.5, s, s);
            		label = mapping[y * w + x + 1] || '?';            		
            		tw = s / 2.0 - context.measureText(label).width / 2.0;
            		th = s / 2.0 + fs / 2.0 - 2;
            		context.fillText(label, x * s + tw, y * s + th );
            	}            	
            }
            context.stroke();
            
          });
    },
    
    changeDimension: function() {
        this.model.save({
          w: this.$(".wall-width").val(),
          h: this.$(".wall-height").val()
        });

        this.$el.removeClass("editing");
    },
    
    startMapping: function() {
        $.post('/led/')
    },    
    
    initialize: function() {
        this.model.on("change", this.render, this);
        $('#test-play').on('click', function(event) {
            $.post('/test/play/');
        });
        $('#test-stop').on('click', function(event) {
            $.post('/test/stop/');
        });
      }
  });

  return Configuration;

});
