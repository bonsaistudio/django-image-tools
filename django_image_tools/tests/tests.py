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

from __future__ import absolute_import
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.conf import settings as django_settings
from django.test import TestCase
from django_image_tools.models import *


def create_dummy_image(filename=u'Test_image', title=u'Title', caption=u'Caption', alt_text=u'Alt Text',
                       credit=u'Credit'):
    im = PILImage.new('RGB', (100, 50))
    im.save(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
    image = Image(filename=filename, title=title, caption=caption, alt_text=alt_text, credit=credit)
    with open(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT), u'rb') as f:
        image.image.save(u'testjpg.jpg', File(f))
    return image


def delete_image(image_object):
    if os.path.exists(path_for_image(image_object)):
        os.remove(path_for_image(image_object))
    image_object.delete()


class SimpleTest(TestCase):

    def setUp(self):
        """
        Add a new image
        """

        create_dummy_image(u'test_image', u'Test', u'Test', u'Test', u'None')

        im = PILImage.new(u'RGB', (200, 100))
        im.save(u'{0}/test_input_bmp.bmp'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
        imagew = Image(filename=u'wasbmp', title=u'Test', caption=u'Test', alt_text=u'Test', credit=u'none.')
        with open(u'{0}/test_input_bmp.bmp'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT), u'rb') as f:
            imagew.image.save(u'{0}/testbmp.bmp'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT), File(f))

        size = Size(name='thumbnail', width=30, height=30, auto=Size.AUTO_NOTHING)
        size.save()
        self.size = size

        longSize = Size(name='very_long', width=200, height=30, auto=Size.AUTO_NOTHING)
        longSize.save()
        self.long = longSize

        tall = Size(name='very_tall', width=30, height=200, auto=Size.AUTO_NOTHING)
        tall.save()
        self.tall = tall

        huge = Size(name='huge', width=2000, height=2000, auto=Size.AUTO_NOTHING)
        huge.save()
        self.huge = huge

        bw = Filter(name='grey_scaled', filter_type=0)
        bw.save()

        self.auto_width = Size(name='auto_width', height=20, auto=Size.AUTO_WIDTH)
        self.auto_width.save()

        self.auto_height = Size(name='auto_height', width=20, auto=Size.AUTO_HEIGHT)
        self.auto_height.save()

        self.imagepath = u'{0}/test_image.jpg'.format(settings.MEDIA_ROOT)
        self.imagewpath = u'{0}/wasbmp.jpg'.format(settings.MEDIA_ROOT)

    def test_auto_width(self):
        image = Image.objects.get(filename=u'test_image')

        self.assertIsNotNone(image.get__auto_width)

        img = PILImage.open(path_for_image_with_size(image, self.auto_width))

        self.assertEqual(img.size[0], 40)
        self.assertEqual(img.size[1], 20)

    def test_auto_height(self):

        image = Image.objects.get(filename=u'test_image')

        self.assertIsNotNone(image.get__auto_height)

        img = PILImage.open(path_for_image_with_size(image, self.auto_height))

        self.assertEqual(img.size[0], 20)
        self.assertEqual(img.size[1], 10)

    def testCreation(self):
        """
        Test that the saving happened
        """
        image = Image.objects.get(filename=u'test_image')
        self.assertTrue(os.path.exists(path_for_image(image)))
        self.assertEqual(Image.objects.all().count(), 2) # There should be two images in the db
        self.assertEqual(Image.objects.all()[0].filename, u'test_image')
        self.assertEqual(path_for_image(image), self.imagepath)

    def testJPGConversion(self):
        """
        Test that the new image has the right name and is in the right directory
        """
        image = Image.objects.get(filename=u'test_image')
        imagew = Image.objects.get(filename=u'wasbmp')

        self.assertEqual(path_for_image(image), self.imagepath)

        self.assertEqual(path_for_image(imagew), self.imagewpath)
        img = PILImage.open(path_for_image(imagew))
        self.assertEqual(img.format, u'JPEG')


    def test_grey_scale(self):
        """
        Test that applying a filter results in a new image created correctly.
        """
        image = Image.objects.get(filename=u'test_image')
        bw = Filter.objects.get(name=u'grey_scaled')

        self.assertFalse(os.path.exists(path_for_image_with_filter_and_size(image, bw, self.size)))
        self.assertEqual(image.get__grey_scaled__thumbnail,
                         media_path_for_image_with_filter_and_size(image, bw, self.size))
        self.assertTrue(os.path.exists(path_for_image_with_filter_and_size(image, bw, self.size)))

    def test_gaussian_blur(self):
        """
        Tests the gaussian blur
        """
        im_filter = Filter(name=u'blurred', filter_type=Filter.GAUSSIAN_BLUR, numeric_parameter=2)
        im_filter.save()

        image = Image.objects.get(filename=u'test_image')

        path = media_path_for_image_with_filter_and_size(image, im_filter, self.size)
        self.assertFalse(os.path.exists(path))
        self.assertEqual(image.get__blurred__thumbnail, path)
        self.assertTrue(os.path.exists(path_for_image_with_filter_and_size(image, im_filter, self.size)))

    def test_original_filter(self):
        """
        Test that applying a filter results in a new image created correctly.
        """
        image = Image.objects.get(filename=u'test_image')
        bw = Filter.objects.get(name=u'grey_scaled')

        self.assertFalse(os.path.exists(path_for_image_with_filter_and_size(image, bw, None)))
        self.assertEqual(image.get__grey_scaled__original,
                         media_path_for_image_with_filter_and_size(image, bw, None))
        self.assertTrue(os.path.exists(path_for_image_with_filter_and_size(image, bw, None)))

    def testRenaming(self):
        """
        Test that an image can be renamed correctly
        """
        image = Image.objects.get(filename=u'test_image')

        image.filename = u'renamed'
        image.save()
        self.assertTrue(os.path.exists(path_for_image(image)))
        self.assertFalse(os.path.exists(self.imagepath))
        image = Image.objects.get(filename=u'renamed')
        image.filename = u'test_image'
        image.save()

    def testResize(self):
        """
        Now add a simple size, and test that the resizing system works
        """
        image = Image.objects.get(filename=u'test_image')

        self.assertEqual(image.get__thumbnail, u'/media/cache/test_image_thumbnail.jpg')
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size)))

    def testLazyCreation(self):
        """
        Test that the new image is created on request
        """
        self.size.width = 250
        self.size.height = 250
        self.size.save()
        image = Image.objects.all()[0]
        self.assertEqual(image.get__thumbnail, u'/media/cache/test_image_thumbnail.jpg')
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size)))

        img = PILImage.open(path_for_image_with_size(image, self.size))
        self.assertTrue(img.size[0] == 250 and img.size[1] == 250)

    def test_rename_exception(self):
        """
        Test that renaming another image with the same name of an existing one will trigger an exception
        """
        image = Image.objects.get(filename=u'test_image')
        image2 = Image.objects.get(filename=u'wasbmp')
        image2.filename = image.filename
        self.assertRaises(ValidationError, image2.save)

    def test_unicode(self):
        self.assertEqual(self.size.__unicode__(), u'thumbnail - (30, 30)')

    def test_filter_unicode(self):
        bw = Filter.objects.get(name=u'grey_scaled')
        self.assertEqual(bw.__unicode__(), u'grey_scaled')

    def test_non_existing_parameters(self):
        image = Image.objects.get(filename=u'test_image')
        self.assertRaises(AttributeError, lambda: image.get__grey_scaled__thbnail)
        self.assertRaises(AttributeError, lambda: image.get__grey_scad__thumbnail)

    def test_double_filter(self):
        image = Image.objects.get(filename=u'test_image')
        self.assertRaises(NotImplementedError, lambda: image.get__grey_scaled__blurred__thumbnail)

    def test_returns_attribute_error(self):
        image = Image.objects.get(filename=u'test_image')
        self.assertRaises(AttributeError, lambda: image.non_existing_property)

    def test_gaussian_blur_parameter_exception(self):
        gaussian_filter = Filter(name=u'gaussian', filter_type=Filter.GAUSSIAN_BLUR)
        self.assertRaises(ValidationError, gaussian_filter.save)
        self.assertRaises(ValidationError, gaussian_filter.clean)

    def test_reserved_keywords_in_size(self):
        error_causing = Size(name=u'huge__with_double_underscore', width=2000, height=2000)
        self.assertRaises(ValidationError, error_causing.save)
        self.assertRaises(ValidationError, error_causing.clean)

    def test_reserved_keywords_in_filters(self):
        error_causing = Filter(name=u'huge__with_double_underscore', filter_type=Filter.GREY_SCALE)
        self.assertRaises(ValidationError, error_causing.save)
        self.assertRaises(ValidationError, error_causing.clean)

    def test_thumbnail(self):
        image = Image.objects.get(filename=u'test_image')
        # When there IS a thumbnail, the code should be this
        self.assertEqual(image.thumbnail(), u'<img src="/media/cache/test_image_thumbnail.jpg" width="100" height="100" />')
        self.size.delete()
        image = Image.objects.get(filename=u'test_image')
        self.assertEqual(image.thumbnail(), u'<img src="/media/test_image.jpg" width="100" height="100" />')

    def test_title(self):
        image = Image.objects.get(filename=u'test_image')
        self.assertEqual(image.__unicode__(), u'Test')

    def test_weird_sizes(self):
        image = Image.objects.get(filename=u'test_image')
        self.assertEqual(image.get__very_long, media_path_for_image_with_size(image, self.long))
        img = PILImage.open(path_for_image_with_size(image, self.long))
        self.assertTrue(img.size[0] == self.long.width and img.size[1] == self.long.height)

        self.assertEqual(image.get__very_tall, media_path_for_image_with_size(image, self.tall))
        img = PILImage.open(path_for_image_with_size(image, self.tall))
        self.assertTrue(img.size[0] == self.tall.width and img.size[1] == self.tall.height)

    def test_upscale_check(self):
        """
        Test that when an image is upscaled, the info is saved onto the db
        """
        image = Image.objects.get(filename=u'test_image')
        self.assertFalse(image.was_upscaled)
        self.assertEqual(image.get__huge, media_path_for_image_with_size(image, self.huge))
        # Now the image was upscaled, so the flag should be true
        image = Image.objects.get(filename=u'test_image')
        self.assertTrue(image.was_upscaled)

    # ----- Settings tests
    def test_media_root_is_set(self):
        mr = django_settings.MEDIA_ROOT
        del django_settings.MEDIA_ROOT
        self.assertRaises(ImproperlyConfigured, settings.update_settings)
        django_settings.MEDIA_ROOT = mr
        settings.update_settings()


    def test_folders_are_created(self):
        if os.listdir(settings.MEDIA_ROOT) != []:
            #Cannot run tests, there are some files in the media root
            self.assertEqual(1, 1, u"Test did not run as the MEDIA_ROOT is not empty")
        else:
            os.remove(settings.MEDIA_ROOT)
            os.remove(settings.UPLOAD_TO)
            self.assertFalse(os.path.exists(settings.MEDIA_ROOT))
            settings.update_settings()
            self.assertTrue(os.path.exists(settings.MEDIA_ROOT))
            self.assertTrue(os.path.exists(settings.UPLOAD_TO))

    def test_settings_fallback(self):
        django_settings.UPLOAD_TO = 'upload_to'
        django_settings.DJANGO_IMAGE_TOOLS_UPLOAD_TO = 'djtupload'

        settings.update_settings()
        self.assertEqual(settings.UPLOAD_TO, 'djtupload')

        del django_settings.UPLOAD_TO
        del django_settings.DJANGO_IMAGE_TOOLS_UPLOAD_TO

        settings.update_settings()
        self.assertEqual(settings.UPLOAD_TO, settings.MEDIA_ROOT)

    def tearDown(self):
        """
        Cleaning up what was created...
        """
        image = Image.objects.get(filename=u'test_image')
        imagew = Image.objects.get(filename=u'wasbmp')

        delete_image(image)
        delete_image(imagew)

        for s in Size.objects.all():
            s.delete()

        # Delete the temporary images
        os.remove(u'{0}/test_input_bmp.bmp'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
        os.remove(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
