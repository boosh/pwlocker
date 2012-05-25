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

        // display the password
        showPassword: function() {
            this.set({"password": this.get('clearPassword')});
        },

        // hide the password
        hidePassword: function() {
            this.set({"password": '********'});
        }
    });

    // define the collection of passwords
    var PasswordCollection = Backbone.Collection.extend({
        model: Password,
        url: '/api/1.0/passwords/'
    });

    // instantiate a password collection
    var Passwords = new PasswordCollection();

    // set up the view for a password
    var PasswordView = Backbone.View.extend({
        tagName: 'tr',

        events: {
            "mouseover .password": "showPassword",
            "mouseout .password": "hidePassword"
        },

        render: function () {
            console.log('Inside PasswordView.render.');
            // template with ICanHaz.js (ich)
            this.el = ich.passwordRowTpl(this.model.toJSON());
            console.log('Password rendered to ' + this.el);
            return this;
        },

        showPassword: function() {
            this.model.showPassword();
        },

        hidePassword: function() {
            this.model.hidePassword();
        }
    });

    var AppView = Backbone.View.extend({
        tagName: 'tbody',
        el: $('#app'),

        initialize: function() {
            
            Passwords.bind('all', this.render, this);
            Passwords.fetch();
        },

        render: function () {
            console.log('Inside AppView.render. Passwords.length = ' + Passwords.length);

            // template with ICanHaz.js (ich)
            Passwords.each(function (password) {
                $(this.el).append(new PasswordView({model: password}).render().el);
            }, this);

            console.log("Rendered to " + this.el);
            return this;
//            this.el = ich.passwordAppTpl(Passwords);
        }
    });

    var app = new AppView();
//    $('#app').html(app.el);
});