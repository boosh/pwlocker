#!/bin/env python
import os
import os.path
import subprocess
import sys

DJANGO_BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
PROJECT_BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

# if there's no venv, create a virtualenv
VENV_DIR = os.path.join(PROJECT_BASE, 'venv')

if not os.path.isdir(VENV_DIR):
    print "Creating virtualenv at " + VENV_DIR
    retcode = subprocess.call(["virtualenv", "--no-site-packages", VENV_DIR])
    
    if retcode:
        print "Problem creating virtualenv. Aborting."
        sys.exit(retcode)

# install dependencies
print "Installing dependencies with pip"
retcode = subprocess.call([os.path.join(VENV_DIR, "bin/pip"), "install", "-r",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")])

if retcode:
    print "Problem installing requirements with pip. Aborting."
    sys.exit(retcode)

# run syncdb to build database
print "Syncing database"
retcode = subprocess.call([os.path.join(VENV_DIR, 'bin/python'),
    os.path.join(DJANGO_BASE, 'manage.py'), "syncdb"])

if retcode:
    print "Problem syncing database. Aborting."
    sys.exit(retcode)

print "Running migrations"
retcode = subprocess.call([os.path.join(VENV_DIR, 'bin/python'),
    os.path.join(DJANGO_BASE, 'manage.py'), "migrate", "--all"])

if retcode:
    print "Problem running migrations. Aborting."
    sys.exit(retcode)

print "Success: Project built"