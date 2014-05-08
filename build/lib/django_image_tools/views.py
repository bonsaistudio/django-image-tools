# Created by Bonsai Studio <info@bonsai-studio.net>
# Copyright (C) Bonsai Studio
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import absolute_import
from django.views.generic import DetailView
from .models import Image


class SingleImage(DetailView):
    model = Image
    template_name = u'single_image.html'


class ComponentImage(DetailView):
    model = Image
    template_name = u'single_image_component.html'
