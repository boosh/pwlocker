import os.path

from settings import *

# production settings

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default']['PASSWORD'] = 'werwfefwefwefwef'

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
MEDIA_ROOT = os.path.join('/home/deploy/projects', PROJECT, 'media')
STATIC_ROOT = os.path.join('/home/deploy/projects', PROJECT, 'static')

SESSION_COOKIE_AGE = 60*60
SESSION_SAVE_EVERY_REQUEST = True