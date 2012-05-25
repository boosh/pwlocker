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

    // set up the view for a password
    var PasswordView = Backbone.View.extend({
//        events: {
//            "mouseover .password": "showPassword",
//            "mouseout .password": "hidePassword"
//        },

        render: function () {
            // template with ICanHaz.js (ich)
            this.el = ich.passwordRowTpl(this.model.toJSON());
            return this;
        }

//        showPassword: function() {
//            this.model.showPassword();
//        },
//
//        hidePassword: function() {
//            this.model.hidePassword();
//        }
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
            this.passwords.bind('all', this.render, this);
            this.passwords.fetch();
        },

        render: function () {
            // template with ICanHaz.js (ich)
            this.passwords.each(function (password) {
                $(this.el).append(new PasswordView({model: password}).render().el);
            }, this);

            return this;
        }
    });

    var app = new AppView();
    $('#app').append(app.render().el);
});