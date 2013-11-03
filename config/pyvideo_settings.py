from richard.settings import *

import mysecrets

import sys
import os

# site_root is the parent directory
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))

# root is this directory
ROOT = os.path.join(SITE_ROOT, 'richard', 'richard')

TEMPLATE_DEBUG = DEBUG = False

SITE_URL = 'http://pyvideo.org'

SITE_TITLE = u'pyvideo.org'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Will Kahn-Greene', 'willg@bluesock.org'),
    ('Carl Superfly Karsten', 'cfkarsten@gmail.com'),
)

MANAGERS = ADMINS

VIDEO_THUMBNAIL_SIZE = (160, 120)
MEDIA_PREFERENCE = ('ogv', 'webm', 'mp4')
API = True
AMARA_SUPPORT = False
PAGES = ['about']
MAX_FEED_LENGTH = 30

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgres_psycopg2',
        'NAME': mysecrets.DB_NAME,
        'USER': mysecrets.DB_USER,
        'PASSWORD': mysecrets.DB_PWD,
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(SITE_ROOT, 'whoosh_index'),
    },
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'staticbase'),
    os.path.join(ROOT, 'static'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = mysecrets.SECRET_KEY

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(ROOT, 'templates'),
)

EMAIL_SUBJECT_PREFIX = '[Django pyvideo]'

SPAM_WORDS = [
    'casino',
    'loans',
    'viagra',
    'valium',
    'proactol',
    'hormone',
    'forex',
    'cigarette',
    'cigarettes',
    'levitra',
    'blackjack',
    'poker',
    'cialis',
    'roulette',
    'propecia',
    'tramadol',
    'insurance',
    'payday',
    'keno',
    'hgh',
    'hair',
    'vegas',
    'ketone',
    'slots',
    'slot',
    'debt',
    'wartrol',
    'provestra',
    'bowtrol',
    'casinos',
    'loan',
    'pills',
    'diet',
    'hosting',
    'review',
    'repair',
    'toner',
    'party',
    'debt',
    'alarm',
    'locksmiths',
    ]

try:
    from pyvideo_settings_local import *
except ImportError:
    pass
