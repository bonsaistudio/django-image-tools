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
from django.core.files import File

from django.test import TestCase
from .models import Image as ImageWrapper
from .models import *


class SimpleTest(TestCase):

    def setUp(self):
        """
        Add a new image
        """
        f = open(u'test_resources/Zerg.jpg')
        image = ImageWrapper(filename=u'test_image', title=u'Test', caption=u'Test', alt_text=u'Test',
                             credit=u'none.')
        image.image.save(u'test.jpg', File(f))
        self.image = image

        f = open(u'test_resources/cone.bmp')
        imagew = ImageWrapper(filename=u'wasbmp', title=u'Test', caption=u'Test', alt_text=u'Test',
                              credit=u'none.')
        imagew.image.save(u'wasbmp.bmp', File(f))
        self.imagew = imagew

        self.imagepath = u'{0}/test_image.jpg'.format(settings.MEDIA_ROOT)
        self.imagewpath = u'{0}/wasbmp.jpg'.format(settings.MEDIA_ROOT)

        size = Size(name=u'thumbnail', width=30, height=30)
        size.save()
        self.size = size

        long = Size(name=u'very_long', width=200, height=30)
        long.save()
        self.long = long

        tall = Size(name=u'very_tall', width=30, height=200)
        tall.save()
        self.tall = tall

        huge = Size(name=u'huge', width=2000, height=2000)
        huge.save()
        self.huge = huge

    def testCreation(self):
        """
        Test that the saving happened
        """
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertTrue(os.path.exists(path_for_image(image)))
        self.assertEqual(ImageWrapper.objects.all().count(), 2) # There should be two images in the db
        self.assertEqual(ImageWrapper.objects.all()[0].filename, u'test_image')
        self.assertEqual(path_for_image(image), self.imagepath)

    def testJPGConversion(self):
        """
        Test that the new image has the right name and is in the right directory
        """
        image = ImageWrapper.objects.get(filename=u'test_image')
        imagew = ImageWrapper.objects.get(filename=u'wasbmp')

        self.assertEqual(path_for_image(image), self.imagepath)

        self.assertEqual(path_for_image(imagew), self.imagewpath)
        img = PILImage.open(path_for_image(imagew))
        self.assertEqual(img.format, u'JPEG')

    def testRenaming(self):
        """
        Test that an image can be renamed correctly
        """
        image = ImageWrapper.objects.get(filename=u'test_image')

        image.filename = u'renamed'
        image.save()
        self.assertTrue(os.path.exists(path_for_image(image)))
        self.assertFalse(os.path.exists(self.imagepath))
        image.filename = u'test_image'
        image.save()

    def testResize(self):
        """
        Now add a simple size, and test that the resizing system works
        """
        image = ImageWrapper.objects.get(filename=u'test_image')

        self.assertEqual(image.get_thumbnail(), u'/media/cache/test_image_thumbnail.jpg')
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size)))

    def testLazyCreation(self):
        """
        Test that the new image is created on request
        """
        self.size.width = 250
        self.size.height = 250
        self.size.save()
        image = ImageWrapper.objects.all()[0]
        self.assertEqual(image.get_thumbnail(), u'/media/cache/test_image_thumbnail.jpg')
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size)))

        img = PILImage.open(path_for_image_with_size(image, self.size))
        self.assertTrue(img.size[0] == 250 and img.size[1] == 250)

    def test_rename_exception(self):
        """
        Test that renaming another image with the same name of an existing one will trigger an exception
        """
        image = ImageWrapper.objects.get(filename=u'test_image')
        image2 = ImageWrapper.objects.get(filename=u'wasbmp')
        image2.filename = image.filename
        self.assertRaises(ValidationError, image2.save)

    def test_unicode(self):
        self.assertEqual(self.size.__unicode__(), u'thumbnail - (30, 30)')

    def test_thumbnail(self):
        image = ImageWrapper.objects.get(filename=u'test_image')
        # When there IS a thumbnail, the code should be this
        self.assertEqual(image.thumbnail(), u'<img src="/media/cache/test_image_thumbnail.jpg" width="100" height="100" />')
        self.size.delete()
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertEqual(image.thumbnail(), u'<img src="/media/test_image.jpg" width="100" height="100" />')

    def test_title(self):
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertEqual(image.__unicode__(), u'Test')

    def test_weird_sizes(self):
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertEqual(image.get_very_long(), media_path_for_image_with_size(image, self.long))
        img = PILImage.open(path_for_image_with_size(image, self.long))
        self.assertTrue(img.size[0] == self.long.width and img.size[1] == self.long.height)

        self.assertEqual(image.get_very_tall(), media_path_for_image_with_size(image, self.tall))
        img = PILImage.open(path_for_image_with_size(image, self.tall))
        self.assertTrue(img.size[0] == self.tall.width and img.size[1] == self.tall.height)

    def test_upscale_check(self):
        """
        Test that when an image is upscaled, the info is saved onto the db
        """
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertFalse(image.was_upscaled)
        self.assertEqual(image.get_huge(), media_path_for_image_with_size(image, self.huge))
        # Now the image was upscaled, so the flag should be true
        image = ImageWrapper.objects.get(filename=u'test_image')
        self.assertTrue(image.was_upscaled)

    def tearDown(self):
        """
        Cleaning up what was created...
        """
        image = ImageWrapper.objects.get(filename=u'test_image')
        imagew = ImageWrapper.objects.get(filename=u'wasbmp')
        image.delete()
        imagew.delete()
        if self.size.pk is not None:
            self.size.delete()
        os.remove(path_for_image(image))
        os.remove(path_for_image(imagew))
