$(function(){
    $('#test-play').on('click', function(event) {
        $.post('/test/play/');
    });
    $('#test-stop').on('click', function(event) {
        $.post('/test/stop/');
    });
    
    
    var EpicWallRouter = Backbone.Router.extend({

        routes:{
            "":"home",
            "configuration":"configuration"
        },

        initialize: function () {
            
        },

        home: function () {
            console.info('home');
            // Since the home view never changes, we instantiate it and render it only once
            if (!this.homeView) {
                this.homeView = new HomeView();
                this.homeView.render();
            }
            $('#content').html(this.homeView.el);
        },

        configuration: function () {
            console.info('config');
            if (!this.configurationView) {
                this.configurationView = new ConfigurationView();
                this.configurationView.render();
            }
            $('#content').html(this.configurationView.el);
        }

    });
    
    
    var HomeView = Backbone.View.extend({

        events: {
            
        },

        initialize: function() {
            
        },

        render: function (eventName) {
            $(this.el).jqotesub($('#tmpl-home'));
            return this;
        }
    });
    
    
    var ConfigurationView = Backbone.View.extend({

        events: {
            
        },

        initialize: function() {
            
        },

        render: function (eventName) {
            $(this.el).jqotesub($('#tmpl-configuration'));
            return this;
        }
    });
    
    
    var router = new EpicWallRouter();
    Backbone.history.start();
});