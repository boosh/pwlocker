Password locker
===============
This is a sample application that demonstrates how to use Django with backbone.js. 

Follow the tutorial at http://10kblogger.wordpress.com/2012/05/25/a-restful-password-locker-with-django-and-backbone-js/

Installation
------------
The code has the following dependencies:

    * Python 2.7
    * virtualenv
    * setuptools
    * fabric

Clone the repository, change into the `pwlocker` directory (containing `settings.py`). Open `settings.py` in your favourite text editor and update the database details to match a database you can connect to. Then just run `fab build` which will create a virtualenv and install all of the required dependencies.
