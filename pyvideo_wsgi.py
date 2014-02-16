# FIXME - this should be part of richard, but it needs
# to check to see if DJANGO_SETTINGS_MODULE exists in the
# env before stomping on it.
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
