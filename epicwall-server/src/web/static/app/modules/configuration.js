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
    
    drawText: function(label, x, y){
        var fs = 20;
        tw = this.gridSize / 2.0 - this.context2d.measureText(label).width / 2.0;
        th = this.gridSize / 2.0 + fs / 2.0 - 2;
        this.context2d.font = "normal " + fs + "px Sans";
        this.context2d.fillText(label, x + tw, y + th);        
    },

    drawMatrix: function(showText) {
      var w = this.model.get("w"), h = this.model.get("h"),
      mapping = this.model.get("mapping"), label = '', tw = 0, th = 0,
      fs = 20;
      var canvas = document.getElementById("myCanvas");
      canvas.width = w * this.gridSize + 1;
      canvas.height = h * this.gridSize + 1;
      this.context2d.clearRect(0, 0, canvas.width, canvas.height);
      this.context2d.strokeStyle = "#ccc";
        
      for (var y = 0; y < h; y++){
        for (var x = 0; x < w; x++){
          this.context2d.rect(x * this.gridSize + 0.5, y * this.gridSize + 0.5, this.gridSize, this.gridSize);
          if(showText){
            label = mapping[y * w + x];
            if(_.isUndefined(label)){
              label = '?';
            }
            this.drawText(label, x * this.gridSize, y * this.gridSize);           
          }
        }
      }
      this.context2d.stroke();
    },
    
    render: function(manage) {
      return manage(this).render().then(function(el) {
        $('.save-mapping').hide();
        $('.abort-mapping').hide();
        $('.next-mapping').hide();
        var canvas = document.getElementById("myCanvas");
        this.context2d = canvas.getContext("2d");        
        this.drawMatrix(true);
      });
    },
    
    changeDimension: function() {
        this.model.save({
          w: this.$(".wall-width").val(),
          h: this.$(".wall-height").val(),
          addressstart: this.$(".address-start").val(),
          addressend: this.$(".address-end").val()
        });
    },
    
    nextMap: function(){
        this.mapstep += 1;
        if(this.mapstep <= this.model.get('addressend')){            
            this.ledStep();
        }else{
            $('.mapstep').text('Done!');
            $('.save-mapping').show();
            $('.next-mapping').hide();
            $('.save-mapping').click($.proxy(function(){
                this.model.save({
                    mapping: this.tempMap
                });
            }, this));          
        } 
    },
    
    clickWall: function(e){
        var x = Math.floor(e.offsetX / this.gridSize),
        y = Math.floor(e.offsetY / this.gridSize), led = 0;
        led = y * this.model.get('w') + x;
        if(_.has(this.tempMap, led)){
            return;
        }
        this.tempMap[led] = this.mapstep;
        this.drawText(this.mapstep, x * this.gridSize, y * this.gridSize);
        this.nextMap();
    },
    
    ledStep: function(){
        $.post('/led/', {ledid: this.mapstep});
        $('.mapstep').text(this.mapstep);
    },
    
    startMapping: function() {
      $('.start-mapping').hide();
      $('.abort-mapping').show();      
      $('.next-mapping').show();  
      this.mapstep = parseInt(this.model.get('addressstart'), 10);
      this.tempMap = {};
      this.drawMatrix(false);      
      this.ledStep();
      $('.abort-mapping').click($.proxy(function(){
          this.render();
      }, this));
      $('.next-mapping').click($.proxy(function(){
          this.nextMap();
      }, this));
      $('#myCanvas').click($.proxy(this.clickWall, this));
            
    },
    
    initialize: function() {
        this.model.on("change", this.render, this);
        this.mapstep = 0;
        this.gridSize = 50.0;
        this.tempMap = {};
      }
  });

  return Configuration;

});
