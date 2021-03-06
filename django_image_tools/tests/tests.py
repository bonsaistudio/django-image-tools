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
from os import listdir
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.conf import settings as django_settings
from django.test import TestCase
from os.path import isfile, join
from django_image_tools.models import *


def create_dummy_image(filename=u'Test_image', title=u'Title', caption=u'Caption', alt_text=u'Alt Text',
                       credit=u'Credit'):
    # Create a dummy 100 x 50 image
    im = PILImage.new('RGB', (100, 50))
    pix = im.load()
    # Add a red pixel so we can test various stuff
    radius = 9
    for i in range(0, radius):
        for j in range(0, radius):
            pix[i, j] = (255, 0, 0)
    im.save(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
    image = Image(filename=filename, title=title, caption=caption, alt_text=alt_text, credit=credit)
    with open(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT), u'rb') as f:
        image.image.save(u'testjpg.jpg', File(f))
    image.save()
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
            imagew.image.save(u'testbmp.bmp', File(f))

        self.size_thumbnail = get_size_with_name('thumbnail')

        self.long = get_size_with_name('very_long')

        self.tall = get_size_with_name('very_tall')

        self.huge = get_size_with_name('huge')

        self.auto_width = get_size_with_name('auto_width')

        self.auto_height = get_size_with_name('auto_height')

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
        bw = get_filter_with_name('grey_scaled')

        self.assertFalse(os.path.exists(path_for_image_with_filter_and_size(image, bw, self.size_thumbnail)))
        self.assertEqual(image.get__grey_scaled__thumbnail,
                         media_path_for_image_with_filter_and_size(image, bw, self.size_thumbnail))
        self.assertTrue(os.path.exists(path_for_image_with_filter_and_size(image, bw, self.size_thumbnail)))

        # Test that the image was converted to grey scale
        im = PILImage.open(path_for_image_with_filter_and_size(image, bw, self.size_thumbnail))
        # Pixel in (1, 1) is red, but in the greyscale version all the channels
        # Should have the same value
        r, g, b = im.getpixel((1, 1))
        self.assertTrue(r == g == b)

    def test_cropping_other(self):
        image = Image.objects.get(filename=u'test_image')

        # Set the crop point to the bottom right
        image.subject_position_vertical = 5
        image.subject_position_horizontal = 5
        image.save()

        # Reload the image
        image = Image.objects.get(filename=u'test_image')

        # Get the thumbnail (which is smaller)
        self.assertIsNotNone(image.get__thumbnail)

        # Open the thumbnail in Pillow
        im = PILImage.open(path_for_image_with_size(image, self.size_thumbnail))

        # Check that the red pixel is still there
        r, g, b = im.getpixel((0, 0))
        # R, G and B values might change a bit but that's the idea
        self.assertTrue(r > 200)
        self.assertTrue(g < 50)
        self.assertTrue(b < 50)


    def test_cropping_center(self):
        image = Image.objects.get(filename=u'test_image')

        # Set the crop point to the top left
        image.subject_position_vertical = 0
        image.subject_position_horizontal = 0
        image.save()

        # Reload the image
        image = Image.objects.get(filename=u'test_image')

        # Get the thumbnail (which is smaller)
        self.assertIsNotNone(image.get__thumbnail)

        # Open the thumbnail in Pillow
        im = PILImage.open(path_for_image_with_size(image, self.size_thumbnail))
        pix = im.load()

        # Due to compression approximation, the g and b values might not be zero, but they should be still lower than r
        r, g, b = pix[0, 0]

        self.assertTrue(r != 0)
        self.assertTrue(g < r)

    def test_gaussian_blur(self):
        """
        Tests the gaussian blur
        """
        im_filter = get_filter_with_name('blurred')

        image = Image.objects.get(filename=u'test_image')

        path = media_path_for_image_with_filter_and_size(image, im_filter, self.size_thumbnail)
        self.assertFalse(os.path.exists(path))
        self.assertIsNotNone(image.get__blurred__original)
        self.assertTrue(os.path.exists(path_for_image_with_filter_and_size(image, im_filter, None)))

        # Image has a red pixel in (1, 1) and the rest is blurred. If it was blurred with radius (2) then the
        # Pixel in coordinates (2, 1) should be reddish, the pixel in (3, 1) should be reddish too, but the pixel in
        # (3, 1) should be black.

        orig = PILImage.open(path_for_image(image))
        blurred = PILImage.open(path_for_image_with_filter_and_size(image, im_filter, None))

        # Check that the R value of the blurred image is about 1/5 of the original value on the same pixel

        r, g, b = orig.getpixel((8, 8))
        r2, g2, b2 = blurred.getpixel((8, 8))

        self.assertAlmostEqual(4.0/5.0 * float(r), r2, None, None, 1.0/5.0 * float(r))

    def test_original_filter(self):
        """
        Test that applying a filter results in a new image created correctly.
        """
        image = Image.objects.get(filename=u'test_image')
        bw = get_filter_with_name('grey_scaled')

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
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size_thumbnail)))

    def testLazyCreation(self):
        """
        Test that the new image is created on request
        """
        image = Image.objects.all()[0]
        self.assertFalse(os.path.exists(path_for_image_with_size(image, self.size_thumbnail)))
        self.assertEqual(image.get__thumbnail, u'/media/cache/test_image_thumbnail.jpg')
        self.assertTrue(os.path.exists(path_for_image_with_size(image, self.size_thumbnail)))

        img = PILImage.open(path_for_image_with_size(image, self.size_thumbnail))
        self.assertTrue(img.size[0] == self.size_thumbnail.width and img.size[1] == self.size_thumbnail.height)

    def test_rename_exception(self):
        """
        Test that renaming another image with the same name of an existing one will trigger an exception
        """
        image = Image.objects.get(filename=u'test_image')
        image2 = Image.objects.get(filename=u'wasbmp')
        image2.filename = image.filename
        self.assertRaises(ValidationError, image2.save)

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

    def test_thumbnail(self):
        image = Image.objects.get(filename=u'test_image')
        # When there IS a thumbnail, the code should be this
        self.assertEqual(image.thumbnail(), u'<img src="/media/cache/test_image_thumbnail.jpg" width="100" height="100" />')
        # Delete thumbnail
        thumbnail_size = settings.DJANGO_IMAGE_TOOLS_SIZES.pop('thumbnail')

        # When there is no thumbnail size, display the original
        image = Image.objects.get(filename=u'test_image')
        self.assertEqual(image.thumbnail(), u'<img src="/media/test_image.jpg" width="100" height="100" />')

        # Put it back
        settings.DJANGO_IMAGE_TOOLS_SIZES['thumbnail'] = thumbnail_size

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
        self.assertTrue(os.path.exists(settings.MEDIA_ROOT))

    def test_convert_to_png_will_not_delete_files(self):
        """
        Tests that even by brutally calling convert_to_png, the method will
        throw an exception since an image with the same name already exists.
        """
        im1 = Image.objects.get(filename=u'test_image')
        im2 = Image.objects.get(filename=u'wasbmp')

        im1.filename = im2.filename

        callable_function = lambda: convert_to_png(None, instance=im1)

        self.assertRaises(ValidationError, callable_function)

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

        # Delete the temporary images
        os.remove(u'{0}/test_input_bmp.bmp'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
        os.remove(u'{0}/test_input.jpg'.format(settings.DJANGO_IMAGE_TOOLS_CACHE_ROOT))
