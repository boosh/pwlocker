import os.path
from datetime import datetime

from fabric.api import env, hosts
from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import local

from lib import *

# This script provides tasks to build a new development environment or
# deploy to production. It is simple. It should include the following:
#
#   - a task to build staging and run tests
#   - a task to push a tarball of code from staging to production
#   - pulling production passwords in from a different repo so prod
#     passwords can remain separate from the main codebase
#   - consider disabling the site (display an upgrade banner) to take the
#     site off line before backing up the db and applying migrations.
#
# See http://www.slideshare.net/lemonad/django-deployment-with-fabric for
# more information/ideas.
#

# path to git repository
env.repo_path = 'ssh://al@95.154.196.59/var/git/repos/healthcms.git'

# get the project name, e.g. healthcms
env.project_name = os.path.basename(os.path.dirname(env.real_fabfile))

# the virtualenv directory name
env.venv_dir = 'venv'

# where all projects are stored on production servers
env.production_projects_directory = 'projects'

# directory to copy database backups to
env.database_backup_dir = '/root/db_backups'

# @todo - add a task to download a backup of the production db

@task
@hosts('localhost')
def build():
    """
    Build a local development environment.
    """
    # where the .git directory is
    env.project_root = os.path.realpath(os.path.join(
        env.real_fabfile, '..', '..'))

    __build_env_dictionary()

    create_virtualenv(env.virtualenv_dir, env.user)
    install_pip_dependencies(env.requirements_path)
    git_init_submodules(env.project_root)
    compile_less_css(env.project_dir)
    django_syncdb(env.project_dir)
    django_migrate_schema(env.project_dir)
    puts(success="Build finished")

@task
def deploy():
    """
    Deploy site to production.

    @todo - make it keep track of the number of deploys/db backups
      so it doesn't end up creating hundreds by mistake

    @todo - Extend this so it will provision new servers by:
       - installing nginx
       - installing supervisord
       - uploading base configurations using files.upload_template
       - creating links in /etc/nginx/conf.d to the project config file
       - doing the same for supervisord
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    env.user = 'deploy'

    # where the .git directory is
    env.project_root = os.path.realpath(os.path.join(
        '/home', env.user, env.production_projects_directory,
        env.project_name, timestamp))

    __build_env_dictionary()

    git_clone(env.repo_path, env.project_root, env.user)
    git_init_submodules(env.project_root)

    create_virtualenv(env.virtualenv_dir, env.user)
    # if we need to install PIL, we need to do it ourselves. It must be
    # installed and patched otherwise we won't have JPEG or PNG support
    conditionally_install_and_patch_pil(env.requirements_path,
        env.virtualenv_dir, os.path.join(env.fab_dir, 'PIL.setup.py.diff'))

    install_pip_dependencies(env.requirements_path)
    compile_less_css(env.project_dir)

# this should only be run on the database server, and migrations should only
# be run once (not on all web servers). Not an issue for now though.
    backup_database(env.project_name, env.project_dir, env.database_backup_dir)
    # from this point on, we're making changes that will affect the live site
# perhaps we should display a banner to disable the site while we perform a
# backup and migration...
    django_syncdb(env.project_dir, True)
    django_migrate_schema(env.project_dir, True)

    django_publish_static_content(env.project_dir)
    roll_site_forward(os.path.dirname(env.project_root))
    restart_services()
    prune_directory(os.path.dirname(env.project_root), 2, 10)
    puts(success="Deployment finished")

def __build_env_dictionary():
    """
    Builds the env dictionary. Everything is relative to the project directory
    (which contains the .git directory).
    """
    # where the manage.py script is
    env.project_dir = os.path.join(env.project_root, env.project_name)

    # the root of the virtualenv
    env.virtualenv_dir = os.path.join(env.project_root, env.venv_dir)

    # the directory containing the requirements file and PIL setup diff
    env.fab_dir = os.path.join(env.project_dir,
        os.path.basename(env.real_fabfile))

    # path to pip's requirements file
    env.requirements_path = os.path.join(env.fab_dir, 'requirements.txt')
