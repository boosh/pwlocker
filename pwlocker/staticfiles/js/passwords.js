// load the following using JQuery's document ready function
$(function(){

    // Password model
    var Password = Backbone.Model.extend({
//        initialize: function() {
//            this.hidePassword();
//        },
//
//        // display the password
//        showPassword: function() {
//            this.set({"maskedPassword": this.get('password')});
//        },
//
//        // hide the password
//        hidePassword: function() {
//            this.set({"maskedPassword": '********'});
//        },

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
            "click a.edit" : "editPassword",
            "click a.destroy" : "remove"
        },

        editPassword: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            alert(event);
        },

        remove: function(event) {
            event.stopImmediatePropagation();
            if (confirm("Are you sure you want to delete this entry?"))
            {
                this.model.remove();
            }
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

    var PasswordListView = Backbone.View.extend({
        tagName: 'tbody',

        initialize: function() {
            // instantiate a password collection
            this.passwords = new PasswordCollection();

            this.passwords.bind('add', this.addOne, this);
            this.passwords.bind('all', this.render, this);
            this.passwords.fetch();
        },

        addOne: function(password) {
            this.$el.prepend(new PasswordView({model: password}).render().el);
            return this;
        },

        addNew: function(password) {
            this.passwords.create(password);
            return this;
        },

        render: function() {
            this.$el.html('');
            this.passwords.each(this.addOne, this);
            return this;
        }
    });

    var AppView = Backbone.View.extend({
        el: '#app',
        events: {
            "click #passwordFormSubmit": "addNew",
            "keydown #passwordForm": "addNewOnEnter"
        },

        initialize: function() {
            this.passwordList = new PasswordListView();
        },

        render: function() {
            this.$el.find('table').append(this.passwordList.render().el);
        },

        addNewOnEnter: function(event) {
            if (event.keyCode == 13)
            {
                return this.addNew(event);
            }
        },

        addNew: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var form = $('#passwordForm');

            var password = {
                title: $(form).find('#id_title').val(),
                username: $(form).find('#id_username').val(),
                password: $(form).find('#id_password').val(),
                url: $(form).find('#id_url').val(),
                notes: $(form).find('#id_notes').val()
            };

            this.passwordList.addNew(password);
            $('#passwordModal').modal('hide');

            // form ready for the next invocation
            $(form).find('#id_title').val('');
            $(form).find('#id_username').val('');
            $(form).find('#id_password').val('');
            $(form).find('#id_url').val('');
            $(form).find('#id_notes').val('');

            return this;
        }
    });

    var app = new AppView();
    app.render();
});