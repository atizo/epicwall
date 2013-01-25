define([
  "app",
  "modules/configuration",
  "modules/animator",
  "modules/animation",
  "modules/artnet"
],

function(app, Configuration, Animator, Animation, Artnet) {
  var Router = Backbone.Router.extend({
    routes: {
      "": "index",
      "config": "config",
      "animations": "animations",
      "artnet": "artnet"
    },

    index: function() {
        $.post('/animator/', {cmd: 'stop'});
        $.post('/artnet/', {cmd: 'stop'});
        app.useLayout("main");
        var indexView = Backbone.View.extend({template: "start"});
        app.layout.setView(".main", new indexView()).render();
    },
    
    config: function() {
        $.post('/animator/', {cmd: 'stop'});
        $.post('/artnet/', {cmd: 'stop'});
        app.useLayout("main");
        app.layout.setView(".main",
          new Configuration.View({model: this.configuration})).render();
        this.configuration.fetch();
    },
    
    animations: function() {
        $.post('/animator/', {cmd: 'stop'});
        $.post('/artnet/', {cmd: 'stop'});
        app.useLayout("main");
        app.layout.setView(".main",
            new Animator.View({
                views: {
                    ".animations": new Animation.Views.List({collection: this.animations})
                }
            })).render();        
          
        this.animations.fetch();
    },
    
    reset: function() {
        $.post('/animator/', {cmd: 'stop'});
        $.post('/artnet/', {cmd: 'stop'});
        if (this.commits.length) {
            this.commits.reset();
        }        
    },
    
    artnet: function() {
        $.post('/animator/', {cmd: 'stop'});
        app.useLayout("main");
        app.layout.setView(".main",
          new Artnet.View({model: this.artnet})).render();
    },
    
    initialize: function() {
        this.configuration = new Configuration.Model();
        this.animations = new Animation.Collection();
    }
  });
  
  return Router;
});
