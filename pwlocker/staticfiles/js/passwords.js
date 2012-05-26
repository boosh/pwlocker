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
            // call back up to the main app passing the current model for it
            // to allow a user to update the details
            this.options.app.editPassword(this.model);
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
            this.$el.prepend(new PasswordView({model: password, app: this.options.app}).render().el);
            return this;
        },

        addNew: function(password) {
            this.passwords.create(password);
            return this;
        },

        updatePassword: function(passwordData) {
            var password = this.passwords.get(passwordData.id);
            if (_.isObject(password))
            {
                // iterate through all the data in passwordData, setting it
                // to the password model
                for (var key in passwordData)
                {
                    // ignore the ID attribute
                    if (key != 'id')
                    {
                        password.set(key, passwordData[key]);
                    }
                }

                // persist the change
                password.save();
            }
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
            "keydown #passwordForm": "handleModalOnEnter",
            "hidden #passwordModal": "prepareForm"
        },

        initialize: function() {
            this.passwordList = new PasswordListView({app: this});
        },

        render: function() {
            this.$el.find('table').append(this.passwordList.render().el);
        },

        /**
         * Allows users to update an existing password
         *
         * @param Password password: A Password Model of the password to edit.
         */
        editPassword: function(password) {
            this.prepareForm(password.toJSON());
            // store the password ID as data on the modal itself
            $('#passwordModal').data('passwordId', password.get('id'));
            $('#passwordModal').modal('show');
        },

        /**
         * Sets up the password form.
         *
         * @param object passwordData: An object containing data to use for the
         * form values. Any fields not present will be set to defaults.
         */
        prepareForm: function(passwordData) {
            passwordData = passwordData || {};
            
            var data = {
                'title': '',
                'username': '',
                'password': '',
                'url': '',
                'notes': ''
            };

            $.extend(data, passwordData);

            var form = $('#passwordForm');
            $(form).find('#id_title').val(data.title);
            $(form).find('#id_username').val(data.username);
            $(form).find('#id_password').val(data.password);
            $(form).find('#id_url').val(data.url);
            $(form).find('#id_notes').val(data.notes);
            
            // clear any previous references to passwordId in case the user
            // clicked the cancel button
            $('#passwordModal').data('passwordId', '');
        },

        handleModal: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            var form = $('#passwordForm');

            var passwordData = {
                title: $(form).find('#id_title').val(),
                username: $(form).find('#id_username').val(),
                password: $(form).find('#id_password').val(),
                url: $(form).find('#id_url').val(),
                notes: $(form).find('#id_notes').val()
            };

            if ($('#passwordModal').data('passwordId'))
            {
                passwordData.id = $('#passwordModal').data('passwordId');
                this.passwordList.updatePassword(passwordData);
            }
            else
            {
                // add or update the password
                this.passwordList.addNew(passwordData);
            }

            // hide the modal
            $('#passwordModal').modal('hide');

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