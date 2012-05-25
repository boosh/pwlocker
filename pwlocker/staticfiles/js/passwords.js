// load the following using JQuery's document ready function
$(function(){

    // Password model
    var Password = Backbone.Model.extend({
        defaults: function() {
            return {
                // just return a default title
                title: "Untitled"
            };
        },

        initialize: function() {
            this.set('clearPassword', this.get('password'));
            this.hidePassword();
        },

        // display the password
        showPassword: function() {
            this.set({"password": this.get('clearPassword')});
        },

        // hide the password
        hidePassword: function() {
            this.set({"password": '********'});
        },

        remove: function() {
            this.destroy();
        }
    });

    // set up the view for a password
    var PasswordView = Backbone.View.extend({
        tagName: 'tr',
        
        events: {
            "mouseover .password": "showPassword",
            "mouseout .password": "hidePassword",
            "click a.destroy" : "remove"
        },

        remove: function(event) {
            event.stopImmediatePropagation();
            this.model.remove();
        },

        render: function () {
            // template with ICanHaz.js (ich)
            $(this.el).html(ich.passwordRowTpl(this.model.toJSON()));
            return this;
        },

        showPassword: function(event) {
            event.stopImmediatePropagation();
            console.log('Showing pw for ' + this.model.get('title'));
            this.model.showPassword();
        },

        hidePassword: function(event) {
            event.stopImmediatePropagation();
            console.log('Hiding pw for ' + this.model.get('title'));
            this.model.hidePassword();
        }
    });

    // define the collection of passwords
    var PasswordCollection = Backbone.Collection.extend({
        model: Password,
        url: '/api/1.0/passwords/'
    });

    var AppView = Backbone.View.extend({
        tagName: 'tbody',

        initialize: function() {
            // instantiate a password collection
            this.passwords = new PasswordCollection();

            this.passwords.bind('add', this.addOne, this);
            this.passwords.bind('all', this.render, this);
//            this.passwords.bind('change', this.render, this);
            this.passwords.fetch();
        },

        addOne: function(password) {
            this.$el.append(new PasswordView({model: password}).render().el);
            return this;
        },

        render: function() {
            this.$el.html('');
            this.passwords.each(this.addOne, this);
            return this;
        }
    });

    var app = new AppView();
    $('#app').append(app.render().el);
});