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
    className: "well",
      
    template: "animation/item",
    
    events: {
        "change .animconf": "changeAnimation",
    },
    
    getEl: function(selector){
        return $(selector, this.$el);
    },
    
    changeAnimation: function() {
        this.getEl('.speed-label').text(this.getEl('#speed').val());
        this.model.save({
            atype: this.getEl('.atypes').val(),
            speed: this.getEl('#speed').val(),
            blend_mode: this.getEl('.blend_modes').val()
            
        });        
    },
    
    serialize: function() {
      return {
        model: this.model
      };
    },
    
    render: function(manage) {
        return manage(this).render().then(function(el){
            var canvas = this.getEl('.preview')[0];
            this.w = this.model.get("w");
            this.h = this.model.get("h");
            this.gridSize = 30;
            canvas.width = this.w * this.gridSize + 1;
            canvas.height = this.h * this.gridSize + 1;
            this.context2d = canvas.getContext("2d");
            this.context2d.strokeStyle = "#ccc";
            var ws = new WebSocket("ws://" + window.location.host + "/stream/");
            ws.onopen = $.proxy(function() {
                ws.send(this.model.get('layer'));
            }, this);
            ws.onmessage = $.proxy(function (evt) {
                var obj = JSON.parse(evt.data);
                var m_canvas = document.createElement('canvas');
                m_canvas.width = 800;
                m_canvas.height = 800;
                var m_context = m_canvas.getContext("2d");
                m_context.lineWidth = 2;
                m_context.strokeStyle = "#ccc";
                for (var y = 0; y < this.h; y++){
                    for (var x = 0; x < this.w; x++){
                        m_context.fillStyle = obj[y * this.w + x];
                        m_context.fillRect(x * this.gridSize + 0.5, y * this.gridSize + 0.5, this.gridSize, this.gridSize);
                    }
                }
                m_context.stroke();
                this.context2d.clearRect(0, 0, 301, 151);
                this.context2d.drawImage(m_canvas, 0, 0);
            }, this);
        });        
    }
  });

  Animation.Views.List = Backbone.View.extend({    

    render: function(manage) {
      this.$el.children().remove();
      this.collection.each(function(commit) {
        this.insertView(new Animation.Views.Item({
          model: commit
        }));
      }, this);

      return manage(this).render();
    },

    cleanup: function() {
      this.collection.off(null, null, this);
    },

    initialize: function() {
        this.collection.on("reset", this.render, this);       
    }
  });

  return Animation;

});