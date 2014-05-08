from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get(key, default):
    return getattr(settings, key, default)


DJANGO_IMAGE_TOOLS_CACHE_DIR = get('DJANGO_IMAGE_TOOLS_CACHE_DIR', 'cache')
MEDIA_URL = get('MEDIA_URL', '/media/')
try:
    UPLOAD_TO = get('UPLOAD_TO', '')
    if UPLOAD_TO is '':
        UPLOAD_TO = settings.DJANGO_IMAGE_TOOLS_UPLOAD_TO
except KeyError:
    raise ImproperlyConfigured('Django Image Tools needs an UPLOAD_TO directory to work properly, set it up in your settings.py')

try:
    MEDIA_ROOT = settings.MEDIA_ROOT
except KeyError:
    raise ImproperlyConfigured('Django Image Tools couldn\'t find the \'MEDIA_ROOT\'. Have you set it up in your settings.py?')
