# Django settings for test project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
    }
}


TIME_ZONE = 'Europe/Riga'
LANGUAGE_CODE = 'en-uk'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
SECRET_KEY = 'v*%a@==!33+n3y6jzn=y(&&i%iq&@2f2q^q6jqgrfv-xv55-#n'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'django_image_tools.tests.urls'
TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django_image_tools', 
)

import django

if django.VERSION[1] < 7:
    INSTALLED_APPS += (
        'south',
    )
    SOUTH_TESTS_MIGRATE = False

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

UPLOAD_TO = os.path.join(PROJECT_ROOT, 'media/upload')

DJANGO_IMAGE_TOOLS_SIZES = {
    'thumbnail': {
        'width': 30,
        'height': 30,
        'auto': None
    },
    'very_long': {
        'width': 200,
        'height': 30,
        'auto': None
    },
    'very_tall': {
        'width': 30,
        'height': 200,
        'auto': None
    },
    'huge': {
        'width': 2000,
        'height': 2000,
        'auto': None
    },
    'auto_width': {
        'width': 0,
        'height': 20,
        'auto': 'WIDTH'
    },
    'auto_height': {
        'width': 20,
        'height': 0,
        'auto': 'HEIGHT'
    },
}

DJANGO_IMAGE_TOOLS_FILTERS = {
    'grey_scaled': {
        'filter_type': 'GREYSCALE'
    },
    'blurred': {
        'filter_type': 'GAUSSIAN_BLUR',
        'value': 5
    }
}
