define([
  "app",
  "backbone",
],

function(app, Backbone) {

  var Artnet = app.module();

  Artnet.View = Backbone.View.extend({
    template: "artnet/overview",
    
    events: {
        "click .start-artnet": "play",
        "click .stop-artnet": "stop"
    },
    
    play: function() {
      $('.stop-artnet').show();
      $('.start-artnet').hide();
      $.post('/artnet/', {cmd: 'play'});
    },
    
    stop: function() {
      $('.start-artnet').show();
      $('.stop-artnet').hide();
      $.post('/artnet/', {cmd: 'stop'});
    },
    
    render: function(manage) {
      return manage(this).render().then(function(el) {
        $('.stop-artnet').hide();
      });
    }
  });

  return Artnet;

});