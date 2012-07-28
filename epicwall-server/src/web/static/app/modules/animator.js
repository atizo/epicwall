define([
  "app",
  "backbone",
],

function(app, Backbone) {

  var Animator = app.module();

  Animator.View = Backbone.View.extend({
    template: "animator/overview",
    
    events: {
        "click .start-anim": "play",
        "click .stop-anim": "stop"
    },
    
    play: function() {
      $('.stop-anim').show();
      $('.start-anim').hide();
      $.post('/animator/', {cmd: 'play'});
    },
    
    stop: function() {
      $('.start-anim').show();
      $('.stop-anim').hide();
      $.post('/animator/', {cmd: 'stop'});
    },
    
    render: function(manage) {
      return manage(this).render().then(function(el) {
        $('.stop-anim').hide();
      });
    }
  });

  return Animator;

});