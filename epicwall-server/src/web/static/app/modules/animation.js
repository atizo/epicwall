define([
  "app",
  "backbone",
],

function(app, Backbone) {

  var Animation = app.module();

  Animation.Model = Backbone.Model.extend({
    defaults: function() {
      return {
        commit: {}
      };
    }
  });

  Animation.Collection = Backbone.Collection.extend({
    model: Animation.Model,

    url: function() {
      return "/animation/";
    },

    initialize: function(models, options) {
      if (options) {
        this.user = options.user;
        this.repo = options.repo;
      }
    }
  });

  Animation.Views.Item = Backbone.View.extend({     
	
	className: "animation",
      
    template: "animation/item",
    
    events: {
        "change .animconf": "changeAnimation",
    },
    
    getEl: function(selector){
        return $(selector, this.$el);
    },
    
    changeAnimation: function() {
        this.getEl('.speed-label').text(this.getEl('#speed').val());
        this.getEl('.opacity-label').text(this.getEl('#opacity').val());
        this.model.save({
            atype: this.getEl('.atypes').val(),
            speed: this.getEl('#speed').val(),
            opacity: this.getEl('#opacity').val(),
            blend_mode: this.getEl('.blend_modes').val()
            
        });        
    },
    
    serialize: function() {
      return {
        model: this.model
      };
    },
    
    drawPreview: function(data) {
    	var m_canvas = document.createElement('canvas');
    	m_canvas.width = this.pw;
    	m_canvas.height = this.ph;
    	var m_context = m_canvas.getContext("2d");
    	m_context.lineWidth = 2;
        m_context.strokeStyle = "#444";
    	for (var i = 0; i < this.pixels.length; i++){
    		m_context.beginPath()
	        m_context.rect(this.pixels[i][0], this.pixels[i][1], this.gw, this.gh);
	        m_context.fillStyle = data[i];
	        m_context.fill();
	        m_context.stroke();
        }
    	
    	this.context2d.clearRect(0, 0, this.pw, this.ph);
    	this.context2d.drawImage(m_canvas, 0, 0);
    },
    
    render: function(manage) {
        return manage(this).render().then(function(el){
            var canvas = this.getEl('.preview')[0];
            canvas.width = this.pw;
            canvas.height = this.ph;
            this.context2d = canvas.getContext("2d");
        });        
    },
    
    initialize: function() {
    	var cw = 260.0, ch = 130.0, w = this.model.get('w'),
    	h = this.model.get('h'), px = 0;
    	this.gw = Math.floor(cw / w);
    	this.gh = Math.floor(ch / h); 
    	this.pixels = [];
    	this.pw = this.gw * w;
    	this.ph = this.gh * h;        
        for (var y = 0; y < h; y++){
        	for (var x = 0; x < w; x++){
        		this.pixels[px] = [x * this.gw, y * this.gh];
        		px +=1;
        	}        	
        }
    }
    
  });

  Animation.Views.List = Backbone.View.extend({    

    render: function(manage) {
      this.$el.children().remove();
      this.collection.each(function(animation) {
        this.insertView(new Animation.Views.Item({
          model: animation
        }));
      }, this);

      return manage(this).render();
    },

    cleanup: function() {
      this.collection.off(null, null, this);
    },

    initialize: function() {
    	this.previews = {};
        this.collection.on("reset", this.render, this);
        var ws = new WebSocket("ws://" + window.location.host + "/stream/");
        ws.onmessage = $.proxy(function (evt) {
            var obj = JSON.parse(evt.data);
            this.views[''][0].drawPreview(obj.previews[0]);
            this.views[''][1].drawPreview(obj.previews[1]);
            this.views[''][2].drawPreview(obj.previews[2]);
            this.views[''][3].drawPreview(obj.previews[3]);
        }, this);
    }
  });

  return Animation;

});