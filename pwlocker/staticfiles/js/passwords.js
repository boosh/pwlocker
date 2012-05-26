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
//            "mouseover .password": "showPassword",
//            "mouseout .password": "hidePassword",
            "click a.edit" : "editPassword",
            "click a.destroy" : "remove"
        },

        editPassword: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            alert('event for ' + this.model.get('id'));
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
        }

//        showPassword: function(event) {
//            event.stopImmediatePropagation();
//            console.log('Showing pw for ' + this.model.get('title'));
//            this.model.showPassword();
//        },
//
//        hidePassword: function(event) {
//            event.stopImmediatePropagation();
//            console.log('Hiding pw for ' + this.model.get('title'));
//            this.model.hidePassword();
//        }
    });

    // define the collection of passwords
    var PasswordCollection = Backbone.Collection.extend({
        model: Password,
        url: '/api/1.0/passwords/'
    });

    /**
     * Manages the list of passwords and related data. Events are only for
     * child nodes of the generated element.
     */
    var PasswordListView = Backbone.View.extend({
        tagName: 'tbody',

        /**
         * Constructor. Takes a reference to the parent view so we can invoke
         * methods on it.
         */
        initialize: function(options) {
            // instantiate a password collection
            this.passwords = new PasswordCollection();

            this.passwords.bind('add', this.addOne, this);
            this.passwords.bind('all', this.render, this);
            this.passwords.fetch();
        },

        addOne: function(password) {
            // pass a reference to the main application into the password view
            // so it can call methods on it
            this.$el.prepend(new PasswordView({model: password, app: this.app}).render().el);
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

    /**
     * View for the overall application. We need this because backbone can only
     * bind events for children of 'el'.
     *
     * In our template our modal is inside #app, so this class handles
     * interaction at the application level rather than strictly with a
     * collection of Passwords (that's the job of the PasswordListView).
     */
    var AppView = Backbone.View.extend({
        el: '#app',
        events: {
            "click #passwordForm :submit": "handleModal",
            "keydown #passwordForm": "handleModalOnEnter"
        },

        initialize: function() {
            this.passwordList = new PasswordListView({app: this});
        },

        render: function() {
            this.$el.find('table').append(this.passwordList.render().el);
        },

        handleModal: function(event) {
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

            // add or update the password
            this.passwordList.addNew(password);

            // clean up the form
            $('#passwordModal').modal('hide');

            // form ready for the next invocation
            $(form).find('#id_title').val('');
            $(form).find('#id_username').val('');
            $(form).find('#id_password').val('');
            $(form).find('#id_url').val('');
            $(form).find('#id_notes').val('');

            return this;
        },

        handleModalOnEnter: function(event) {
            // process the modal if the user pressed the ENTER key
            if (event.keyCode == 13)
            {
                return this.handleModal(event);
            }
        }
    });

    var app = new AppView();
    app.render();
});