// load the following using JQuery's document ready function
$(function(){

    // Password model
    var Password = Backbone.Model.extend({
        initialize: function() {
            this.hidePassword();
        },

        // display the password
        showPassword: function() {
            this.set({"maskedPassword": this.get('password')});
        },

        // hide the password
        hidePassword: function() {
            this.set({"maskedPassword": '********'});
        },

        remove: function(options) {
            mergedOptions = {wait: true};
            $.extend(mergedOptions, options);
            this.destroy(mergedOptions);
        },

        validate: function(attrs) {
            if (attrs.title.length == 0 || attrs.password.length == 0)
            {
                return "Please enter a title and a password";
            }

            if (attrs.url)
            {
                var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
                if (!re.test(attrs.url))
                {
                    return "Please enter a valid URL";
                }
            }
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
            // call back up to the main app passing the current model for it
            // to allow a user to update the details
            this.options.app.editPassword(this.model);
        },

        remove: function(event) {
            event.stopImmediatePropagation();
            event.preventDefault();
            if (confirm("Are you sure you want to delete this entry?"))
            {
                this.model.remove({error: function(model, response) {
                        if (response.status == 403) {
                            alert("You don't have permission to delete that data");
                        }
                        else {
                            alert("Unable to delete that data");
                        }
                    }
                });
            }
        },

        render: function () {
            // template with ICanHaz.js (ich)
            $(this.el).html(ich.passwordRowTpl(this.model.toJSON()));
            return this;
        },

        showPassword: function(event) {
            event.stopImmediatePropagation();
            this.model.showPassword();
        },

        hidePassword: function(event) {
            event.stopImmediatePropagation();
            this.model.hidePassword();
        }
    });

    // define the collection of passwords
    var PasswordCollection = Backbone.Collection.extend({
        model: Password,
        url: '/api/1.0/passwords/',

        // maintain ordering by password title
        comparator: function(obj1, obj2) {
            return obj1.get('title').localeCompare(obj2.get('title'));
        }
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

            this.passwords.bind('all', this.render, this);
            this.passwords.fetch();
        },

        addOne: function(password) {
            // pass a reference to the main application into the password view
            // so it can call methods on it
            this.$el.append(new PasswordView({model: password, app: this.options.app}).render().el);
            return this;
        },

        addNew: function(password, options) {
            mergedOptions = {wait: true};
            $.extend(mergedOptions, options);
            this.passwords.create(password, mergedOptions);
            return this;
        },

        updatePassword: function(passwordData, options) {
            mergedOptions = {wait: true};
            $.extend(mergedOptions, options);
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
                password.save({}, mergedOptions);
                this.passwords.sort();
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
    var PasswordPanelView = Backbone.View.extend({
        el: '#passwordPanel',
        events: {
            "click #passwordForm :submit": "handleModal",
            "keydown #passwordForm": "handleModalOnEnter",
            "hidden #passwordModal": "prepareForm"
        },

        initialize: function() {
            this.passwordList = new PasswordListView({app: this});
        },

        displayError: function(model, response) {
            var that = this;
            if (response.status == 403) {
                alert("You don't have permission to edit that data");
            }
            else {
                alert("Unable to create or edit that data. Please make sure you entered valid data.");
            }
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

            // create an array of the selected shares
            var shares = _.map(data.shares, function(elem){
                return elem.id;
            });

            var value;
            $(form).find(':checkbox').each(function(){
                value = $(this).attr('value');
                // for each checkbox, see if the value is in the 'shares' array
                for (var i in shares)
                {
                    if (value == shares[i])
                    {
                        $(this).prop('checked', true);
                        return;
                    }
                }

                // otherwise uncheck it
                $(this).prop('checked', false);
            });

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
                notes: $(form).find('#id_notes').val(),
                shares: $(form).find(':checked').map(function() {
                    return $(this).attr('value');
                }).get()
            };

            if ($('#passwordModal').data('passwordId'))
            {
                passwordData.id = $('#passwordModal').data('passwordId');
                this.passwordList.updatePassword(passwordData, { error: this.displayError });
            }
            else
            {
                // add or update the password
                this.passwordList.addNew(passwordData, { error: this.displayError });
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

    var app = new PasswordPanelView();
    app.render();

    // Setup $.ajax to always send an X-CSRFToken header:
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    $(document).ajaxSend(function(e, xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    });
});