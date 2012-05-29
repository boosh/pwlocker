// load the following using JQuery's document ready function
$(function(){

    // Contact model
    var Contact = Backbone.Model.extend({
        remove: function(options) {
            mergedOptions = {wait: true};
            $.extend(mergedOptions, options);
            this.destroy(mergedOptions);
        }
    });

    // set up the view for a contact
    var ContactView = Backbone.View.extend({
        tagName: 'tr',
        
        events: {
            "click a.destroy" : "remove"
        },

        remove: function(event) {
            event.stopImmediatePropagation();
            event.preventDefault();
            if (confirm("Are you sure you want to delete this contact?"))
            {
                var that = this;
                
                this.model.remove({error: function(model, response) {
                        if (response.status == 403) {
                            alert("You don't have permission to delete that data");
                        }
                        else {
                            alert("Unable to delete that data");
                        }
                    },
                    success: function() {
                        // update the form options - a little hacky, but oh well
                        $('#passwordForm').find(':checkbox').remove();
                        $('#passwordForm').find('.checkbox').remove();

                        var shareOptions = new Array();

                        that.options.collection.each(function(data){
                            shareOptions.push(ich.shareOption(data.toJSON(), true));
                        });

                        $(shareOptions.join('')).insertAfter('#id_notes');
                    }
                });
            }
        },

        render: function () {
            // template with ICanHaz.js (ich)
            $(this.el).html(ich.contactRowTpl(this.model.toJSON()));
            return this;
        }
    });

    // define the collection of contacts
    var ContactCollection = Backbone.Collection.extend({
        model: Contact,
        url: '/api/1.0/passwordcontacts/',

        // maintain ordering by first_name
        comparator: function(obj1, obj2) {
            return obj1.get('to_user').first_name.localeCompare(obj2.get('to_user').first_name);
        }
    });

    /**
     * Manages the list of contacts.
     */
    var ContactListView = Backbone.View.extend({
        tagName: 'tbody',

        /**
         * Constructor. Takes a reference to the parent view so we can invoke
         * methods on it.
         */
        initialize: function(options) {
            // instantiate a password collection
            this.collection = new ContactCollection();

            this.collection.bind('all', this.render, this);
            this.collection.fetch();
        },

        addOne: function(contact) {
            this.$el.append(new ContactView({model: contact, collection: this.collection}).render().el);
            return this;
        },

        addNew: function(data, options) {
            mergedOptions = {wait: true};
            $.extend(mergedOptions, options);

            var contact = {
                to_user: data.id
            };

            this.collection.create(contact, mergedOptions);
            return this;
        },

        render: function() {
            this.$el.html('');
            this.collection.each(this.addOne, this);
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
    var ContactPanelView = Backbone.View.extend({
        el: '#contactPanel',
        events: {
            "click #contactPanel :submit": "handleSearch",
            "keydown #contactPanel :input[type=text]": "handleSearchOnEnter"
        },

        initialize: function() {
            this.dataList = new ContactListView({app: this});
        },

        displayError: function(model, response) {
            if (response.status == 403) {
                alert("You don't have permission to edit that data");
            }
            else {
                alert("Unable to create or edit that data. Please make sure you entered valid data.");
            }
        },

        render: function() {
            this.$el.find('table').append(this.dataList.render().el);
        },

        handleSearch: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();

            var username = $('#userSearch').val();

            var that = this;

            // perform a GET request to the userSearch service and if it
            // returns a user, create a new PasswordContact
            $.ajax({
                url: '/api/1.0/user/' + username,
                dataType: 'json',
                success: function(data, textStatus, jqXHR) {
                    that.dataList.addNew(data, {success: function() {
                        $('#userSearch').val('');

                        // update the form options
                        $('#passwordForm').find(':checkbox').remove();
                        $('#passwordForm').find('.checkbox').remove();

                        var shareOptions = new Array();

                        that.dataList.collection.each(function(data){
                            shareOptions.push(ich.shareOption(data.toJSON(), true));
                        });

                        $(shareOptions.join('')).insertAfter('#id_notes');
                    }});
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.status) {
                        alert("Sorry, we couldn't find that user");
                    }
                    else {
                        alert("There was a problem searching for that user.");
                    }
                }
            });

            return this;
        },

        handleSearchOnEnter: function(event) {
            // process the modal if the user pressed the ENTER key
            if (event.keyCode == 13)
            {
                return this.handleSearch(event);
            }
        }
    });

    var contactPanel = new ContactPanelView();
    contactPanel.render();
});