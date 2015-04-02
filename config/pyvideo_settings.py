import os

from richard.config.settings import Prod, BASE_DIR


PYVIDEO_ROOT = os.path.dirname(os.path.dirname(__file__))


class Pyvideo(Prod):
    """pyvideo.org production environment"""
    SITE_URL = 'http://pyvideo.org'

    ALLOWED_HOSTS = [u'pyvideo.org', u'www.pyvideo.org']
    BROWSERID_AUDIENCES = ['http://' + host for host in ALLOWED_HOSTS]

    SITE_TITLE = u'pyvideo.org'

    ADMINS = (
        # ('Your Name', 'your_email@example.com'),
        ('Will Kahn-Greene', 'willg@bluesock.org'),
        ('Sheila Miguez', 'shekay@pobox.com'),
        # ('Carl Superfly Karsten', 'cfkarsten@gmail.com'),
    )

    SERVER_EMAIL = 'noreply-error@pyvideo.org'

    MANAGERS = ADMINS

    AMARA_SUPPORT = True
    API = True
    PAGES = ['about']
    MAX_FEED_LENGTH = 30
    VIDEO_THUMBNAIL_SIZE = (160, 120)

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
        },
    }

    STATICFILES_DIRS = (
        # Add pyvideo staticbase for additional static files.
        os.path.join(PYVIDEO_ROOT, 'staticbase'),
    )

    TEMPLATE_DIRS = (
        os.path.join(PYVIDEO_ROOT, 'templates'),
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


class DevPyvideo(Pyvideo):
    """dev.pyvideo.org stage environment"""
    SITE_URL = 'http://dev.pyvideo.org'
    ALLOWED_HOSTS = [u'dev.pyvideo.org', u'dev.pyvideo.org:80']
    BROWSERID_AUDIENCES = ['http://dev.pyvideo.org', 'http://dev.pyvideo.org:80']
    SITE_TITLE = u'dev.pyvideo.org'

    EMAIL_SUBJECT_PREFIX = '[Django dev.pyvideo]'


class PyvideoLocal(Pyvideo):
    """pyvideo environment for local development"""
    DEBUG = True
    TEMPLATE_DEBUG = True

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
        },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django': {
                'handlers':['console'],
                'propagate': True,
                'level':'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }

    SITE_URL = 'http://127.0.0.1:8000'
    BROWSERID_AUDIENCES = ['http://127.0.0.1:8000', 'http://localhost:8000']
