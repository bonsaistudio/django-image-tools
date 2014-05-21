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
