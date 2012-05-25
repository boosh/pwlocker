# -*- coding: utf-8 -*-
from fabric import colors
from fabric.api import env, sudo
from fabric.api import puts as fabric_puts
from fabric.context_managers import settings
from fabric.operations import run
from fabric.utils import abort

"""
Functions in this file are utilities that remove complexity from the
functions in lib.py.
"""

def puts(info=None, success=None, warn=None, error=None):
    """
    Print a string in different colours
    """
    if info:
        fabric_puts(colors.cyan(info))
    elif success:
        fabric_puts(colors.green(success))
    elif warn:
        fabric_puts(colors.yellow(warn))
    elif error:
        fabric_puts(colors.red(error))

def check_on_path(binary):
    """
    Confirms that named binary is installed system-wide.

    @todo - Fix this. It doesn't work.
    """
    with settings(warn_only=True):
        if run("type '%s'" % binary).failed:
            puts(error="Error: %s is not on the path" % binary)
            abort("Aborting")

def create_directories(path, user, permission='0750', group=None):
    """
    Create directories owned by the named user and group and with the
    given permissions
    """
    group = group or user

    if user == env.user:
        run("mkdir -p %s" % path)
    else:
        sudo("mkdir -p %s" % path)

    sudo("chown -R %s:%s %s" % (user, group, path))
    sudo("chmod -R %s %s" % (permission, path))

def activate_venv():
    """
    Returns a string that will activate the venv which can be used as a
    prefix to other commands
    """
    return "source %s/bin/activate" % env.virtualenv_dir
