# Created by Bonsai Studio <info@bonsai-studio.net>
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (C) Bonsai Studio

import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get(key, default):
    return getattr(settings, key, default)

DJANGO_IMAGE_TOOLS_CACHE_DIR = get('DJANGO_IMAGE_TOOLS_CACHE_DIR', 'cache')
DJANGO_IMAGE_TOOLS_SIZES = get('DJANGO_IMAGE_TOOLS_SIZES', {'thumbnail': {'width': 50, 'height': 50}})
DJANGO_IMAGE_TOOLS_FILTERS = get('DJANGO_IMAGE_TOOLS_FILTERS', {})
MEDIA_URL = get('MEDIA_URL', '/media/')
DJANGO_IMAGE_TOOLS_CACHE_ROOT = ''
MEDIA_ROOT = ''
UPLOAD_TO = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


def update_settings():
    global DJANGO_IMAGE_TOOLS_CACHE_DIR
    DJANGO_IMAGE_TOOLS_CACHE_DIR = get('DJANGO_IMAGE_TOOLS_CACHE_DIR', 'cache')
    global MEDIA_URL
    MEDIA_URL = get('MEDIA_URL', '/media/')
    global DJANGO_IMAGE_TOOLS_CACHE_ROOT
    global MEDIA_ROOT
    global UPLOAD_TO
    global DJANGO_IMAGE_TOOLS_SIZES
    global DJANGO_IMAGE_TOOLS_FILTERS


    try:
        MEDIA_ROOT = settings.MEDIA_ROOT
    except AttributeError:
        raise ImproperlyConfigured(u'Django Image Tools couldn\'t find the \'MEDIA_ROOT\'. '
                                   u'Have you set it up in your settings.py?')

    if not os.path.exists(MEDIA_ROOT):
        os.makedirs(MEDIA_ROOT)

    DJANGO_IMAGE_TOOLS_CACHE_ROOT = os.path.join(MEDIA_ROOT, DJANGO_IMAGE_TOOLS_CACHE_DIR)

    if not os.path.exists(DJANGO_IMAGE_TOOLS_CACHE_ROOT):
        os.makedirs(DJANGO_IMAGE_TOOLS_CACHE_ROOT)

    UPLOAD_TO = get('UPLOAD_TO', '')
    if hasattr(settings, 'DJANGO_IMAGE_TOOLS_UPLOAD_TO'):
        UPLOAD_TO = settings.DJANGO_IMAGE_TOOLS_UPLOAD_TO
    if UPLOAD_TO is '':
        UPLOAD_TO = settings.MEDIA_ROOT

    if not os.path.exists(UPLOAD_TO):
        os.makedirs(UPLOAD_TO)



update_settings()