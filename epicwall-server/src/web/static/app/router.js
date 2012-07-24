define([
  "app",
  "modules/configuration"
],

function(app, Configuration) {
  var Router = Backbone.Router.extend({
    routes: {
      "": "index",
      "config": "config"
    },

    index: function() {
    	app.useLayout("main");
    	var indexView = Backbone.View.extend({template: "start"});
    	app.layout.setView(".main", new indexView()).render({'haha': 'dfasdfa'});
    },
    
    config: function() {
        app.useLayout("main");        
        app.layout.setView(".main",
        		new Configuration.View({model: this.configuration})).render();
        this.configuration.fetch();
    },
    
    initialize: function() {
        this.configuration = new Configuration.Model();
    }    
  });
  
  return Router;
});
