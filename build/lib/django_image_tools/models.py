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
import hashlib
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image as PILImage, ImageFilter
import os
from django.db.models.signals import post_save, post_init, post_delete
from . import settings

PARAMS_SEPARATOR = u'__'
FUNCTION_PREFIX = u'get{0}'.format(PARAMS_SEPARATOR)
ORIGINAL_KEYWORD = u'original'



class Size(models.Model):
    name = models.CharField(max_length=30)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u'{0} - ({1}, {2})'.format(self.name, self.width, self.height)

    def clean(self):
        if PARAMS_SEPARATOR in self.name:
            raise ValidationError(u'Sorry. Your name cannot contain the string \'{sep}\','
                                  u' as it is reserved for internal purposes'.format(sep=PARAMS_SEPARATOR))

    def save(self, *args, **kwargs):
        if PARAMS_SEPARATOR in self.name:
            raise ValidationError(u'Sorry. Your name cannot contain the string \'{sep}\','
                                  u' as it is reserved for internal purposes'.format(sep=PARAMS_SEPARATOR))
        super(Size, self).save(*args, **kwargs)


class Filter(models.Model):
    GREY_SCALE = 0
    GAUSSIAN_BLUR = 1
    available_filters = (
        (GREY_SCALE, u'Grey scale'),
        (GAUSSIAN_BLUR, u'Gaussian Blur'),
    )
    name = models.CharField(max_length=30)

    filter_type = models.PositiveSmallIntegerField(choices=available_filters, help_text=u'The type of filter to apply')
    numeric_parameter = models.FloatField(verbose_name=u'Numeric Parameter', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def clean(self):
        if PARAMS_SEPARATOR in self.name:
            raise ValidationError(u'Sorry. Your name cannot contain the string \'{sep}\','
                                  u' as it is reserved for internal purposes'.format(sep=PARAMS_SEPARATOR))
        if self.filter_type == self.GAUSSIAN_BLUR and self.numeric_parameter is None:
            raise ValidationError(u'Gaussian Blur needs the parameter to be specified')

    def save(self, *args, **kwargs):
        if PARAMS_SEPARATOR in self.name:
            raise ValidationError(u'Sorry. Your name cannot contain the string \'{sep}\','
                                  u' as it is reserved for internal purposes'.format(sep=PARAMS_SEPARATOR))
        super(Filter, self).save(*args, **kwargs)


class Image(models.Model):
    choices_V = (
        (0, u'Top'),
        (1, u'1/3'),
        (2, u'Center'),
        (3, u'2/3'),
        (4, u'Bottom')
    )
    choices_H = (
        (0, u'Left'),
        (1, u'1/3'),
        (2, u'Center'),
        (3, u'2/3'),
        (4, u'Right')
    )
    image = models.ImageField(upload_to=settings.UPLOAD_TO, help_text=u'uploading an image will take time. DO NOT PUSH THE SAVE BUTTON AGAIN UNTIL THE IMAGE HAS BEEN SAVED!')
    checksum = models.CharField(max_length=32)
    filename = models.SlugField(help_text=u'If you want to rename the image, write here the new filename',
                                validators=[RegexValidator(regex=r'^[A-Za-z\-\_0-9]*$',
                                                          message=u'Filename can only contain letters, '
                                                                  u'numbers and \'-\'.'
                                                                  u'No extensions allowed (I\'ll put it for you'), ]
    )
    subject_position_horizontal = models.PositiveSmallIntegerField(choices=choices_H,
                                                                   default=2,
                                                                   verbose_name=u'Subject Horizontal Position',
                                                                   help_text=u'The system will create other images'
                                                                             u'from this, based on the '
                                                                             u'image sizes needed.'
                                                                             u'In some cases, it is necessary to crop'
                                                                             u'the image. By selecting where the '
                                                                             u'subject is, the cropping'
                                                                             u'can be more accurate.')
    subject_position_vertical = models.PositiveSmallIntegerField(choices=choices_V,
                                                                 default=2,
                                                                 verbose_name=u'Subject Vertical Position',
                                                                 help_text=u'The system will create other images'
                                                                           u'from this, based on the '
                                                                           u'image sizes needed.'
                                                                           u'In some cases, it is necessary to crop'
                                                                           u'the image. By selecting where the '
                                                                           u'subject is, the cropping'
                                                                           u'can be more accurate.')
    was_upscaled = models.BooleanField(default=False, verbose_name=u'insufficient_resolution')

    title = models.CharField(max_length=120,
                             help_text=u'In some pages it might be necessary to display some informations.')
    caption = models.TextField()
    alt_text = models.CharField(max_length=120,
                                help_text=u'This is the text that allows blind people (and google) know '
                                          u'what the image is about ')

    credit = models.TextField(null=True, blank=True)

    def thumbnail(self):
        if hasattr(self, u'get__thumbnail'):
            return u'<img src="{thumbnail_path}" width="100" height="100" />'.format(
                thumbnail_path=self.get__thumbnail
            )
        else:
            return u'<img src="{thumbnail_path}" width="100" height="100" />'.format(
                thumbnail_path=self.get__original
            )
    thumbnail.allow_tags = True

    def subject_coordinates(self):
        h = self.image.width * (self.subject_position_horizontal / float(4))
        v = self.image.height * (self.subject_position_vertical / float(4))
        return h, v

    def __unicode__(self):
        return self.title

    def __getattribute__(self, name):
        try:
            attr = super(Image, self).__getattribute__(name)
            return attr
        except AttributeError:
            if name[0:len(FUNCTION_PREFIX)] == FUNCTION_PREFIX:
                params = name[len(FUNCTION_PREFIX):].split(PARAMS_SEPARATOR)
                if len(params) > 2:
                    raise NotImplementedError(u'Multiple filters are not yet implemented')
                else:
                    if len(params) == 1:
                        """
                        If there's only one parameter, it's the size. Check if the size exists
                        """
                        size = None
                        if params[0] != ORIGINAL_KEYWORD:
                            try:
                                size = Size.objects.get(name=params[0])
                            except Size.DoesNotExist:
                                raise AttributeError
                        """
                        Return the requested size
                        """
                        return get_image_on_request(self, size)
                    else:
                        """
                        Exactly two parameters. This means that the first one is a filter and the second one is a size.
                        """
                        try:
                            image_filter = Filter.objects.get(name=params[0])
                        except Filter.DoesNotExist:
                            raise AttributeError
                        size = None
                        if params[1] != ORIGINAL_KEYWORD:
                            try:
                                size = Size.objects.get(name=params[1])
                            except Size.DoesNotExist:
                                raise AttributeError

                        """
                        Return the appropriate filter and size.
                        """
                        return get_image_with_filter_and_size(self, image_filter, size)
            else:
                super(models.Model, self).__getattribute__(name)

    def save(self, *args, **kwargs):
        if os.path.exists(path_for_image(self)) and md5Checksum(path_for_image(self)) != self.checksum:
            raise ValidationError(u'An image with the same name already exists!')
        super(Image, self).save(*args, **kwargs)



    def save_bypassing_signals(self):
        #Save changes to DB, but to avoid triggering this same method again, first disconnect it
        post_save.disconnect(convert_to_png, Image)
        self.save()
        #Now hook the post_save back up
        post_save.connect(convert_to_png, Image)


def md5Checksum(filePath):
    with open(filePath, u'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def rescale_image(img, nsize, crop_point):
    if not crop_point:
        crop_point = (int(round(img.size[0]/float(2))),
                      int(round(img.size[1]/float(2))))
    # First of all, I'm rescaling to whatever the biggest size is
    osize = (img.size[0], img.size[1])
    original_width, original_height = (float(img.size[0]), float(img.size[1]))

    new_width, new_height = (float(nsize[0]), float(nsize[1]))

    original_ratio = original_width/original_height
    new_ratio = new_width/new_height

    if original_ratio < new_ratio:
        #Resize by height
        first_step_height = original_width/new_ratio
        first_step_width = original_width
        first_step_size = (first_step_width,first_step_height)
    else:
        #Resize by width
        first_step_width = new_ratio*original_height
        first_step_height = original_height
        first_step_size = (first_step_width, first_step_height)

    #Recalculate the crop point to the new image sizes..
    crop_x, crop_y = crop_point
    rect_x = crop_x - first_step_width/2
    rect_y = crop_y - first_step_height/2

    if rect_x < 0:
        #Crop rect overflows to the left
        rect_x = 0
    elif rect_x + first_step_width > original_width:
        #Crop rect overflows to the right
        rect_x -= (rect_x + first_step_width) - original_width
    if rect_y < 0:
        #Crop rect overflows to the top
        rect_y = 0
    elif rect_y + first_step_height > original_height:
        rect_y -= (rect_y + first_step_height) - original_height

    img = img.crop(
        (
            int(rect_x),
            int(rect_y),
            int(rect_x + first_step_width),
            int(rect_y + first_step_height),
        )
    )
    return img.resize(nsize, PILImage.ANTIALIAS)


def delete_image_with_size(image, size):
    path = path_for_image_with_size(image, size)
    if os.path.exists(path):
        os.remove(path)


def delete_image_with_filter_and_size(image, im_filter, size):
    path = path_for_image_with_filter_and_size(image, im_filter, size)
    if os.path.exists(path):
        os.remove(path)


def delete_images_for_size(size):
    for image in Image.objects.all():
        delete_image_with_size(image, size)
        for im_filter in Filter.objects.all():
            delete_image_with_filter_and_size(image, im_filter, size)


def delete_sizes_for_image(image):
    for size in Size.objects.all():
        delete_image_with_size(image, size)
        for im_filter in Filter.objects.all():
            delete_image_with_filter_and_size(image, im_filter, size)


def delete_images_for_filter(im_filter):
    for image_object in Image.objects.all():
        delete_image_with_filter_and_size(image_object, im_filter, None)
    for size in Size.objects.all():
        for image_object in Image.objects.all():
            delete_image_with_filter_and_size(image_object, im_filter, size)


def delete_filters_for_image(image):
    for im_filter in Filter.objects.all():
        delete_image_with_filter_and_size(image, im_filter, None)
    for size in Size.objects.all():
        for im_filter in Filter.objects.all():
            delete_image_with_filter_and_size(image, im_filter, size)


def path_for_image_with_filter_and_size(image, im_filter, size):
    return u'{0}/{1}/{2}'.format(settings.MEDIA_ROOT, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                 image_with_filter_and_size(image, im_filter, size))


def path_for_image_with_size(image, size):
    if size is None:
        return path_for_image(image)
    return u'{0}/{1}/{2}'.format(settings.MEDIA_ROOT, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                 image_with_size(image, size))


def media_path_for_image(image):
    filename, extension = os.path.splitext(os.path.basename(image.image.name))
    return u'{0}{1}{2}'.format(settings.MEDIA_URL, filename, extension)


def media_path_for_image_with_size(image, size):
    return u'{0}{1}/{2}'.format(settings.MEDIA_URL, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                image_with_size(image, size))


def media_path_for_image_with_filter_and_size(image_object, im_filter, size):
    return u'{0}{1}/{2}'.format(settings.MEDIA_URL, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                image_with_filter_and_size(image_object, im_filter, size))


def current_path_for_image(imageObject):
    return imageObject.image.file.name


def path_for_image(imageObject, force_extension=None):
    filename, extension = os.path.splitext(os.path.basename(imageObject.image.name))
    if force_extension is not None:
        extension = force_extension
    return u'{0}/{1}{2}'.format(settings.MEDIA_ROOT, imageObject.filename, extension)


def image_with_size(image, size):
    filename, extension = os.path.splitext(os.path.basename(image.image.name))
    return u'{0}_{1}{2}'.format(filename, size.name, extension)


def image_with_filter_and_size(image, im_filter, size):
    # If size is None, then we're fetching the original.
    sizename = u'original'
    if size is not None:
        sizename = size.name
    filename, extension = os.path.splitext(os.path.basename(image.image.name))
    return u'{0}_{1}_{2}{3}'.format(filename, im_filter.name, sizename, extension)


def render_image_with_size(imageObject, size):
    pilImage = PILImage.open(path_for_image(imageObject))
    resizedImage = rescale_image(pilImage,
        (size.width, size.height),
        imageObject.subject_coordinates())
    #If the image is being resized to a bigger scale, set the was_upscaled flag
    if pilImage.size[0] < size.width or pilImage.size[1] < size.height:
        imageObject.was_upscaled=True
        imageObject.save_bypassing_signals()
    image_path = path_for_image_with_size(imageObject, size)
    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))
    resizedImage.save(image_path)


def grey_scale(image_object, im_filter, size):
    # Apply greyscale
    pil_image = PILImage.open(path_for_image_with_size(image_object, size))
    pil_image = pil_image.convert('LA').convert('RGB')
    pil_image.save(path_for_image_with_filter_and_size(image_object, im_filter, size))


def gaussian_blur(image_object, im_filter, size):
    #Open image
    pil_image = PILImage.open(path_for_image_with_size(image_object, size))
    #Apply filter
    # Gaussian blur gets the numeric parameter as the radius.
    pil_image = pil_image.filter(ImageFilter.GaussianBlur(im_filter.numeric_parameter))
    #Save image to its correct path
    pil_image.save(path_for_image_with_filter_and_size(image_object, im_filter, size))


def render_image_with_filter_and_size(image_object, im_filter, size):
    if not os.path.exists(path_for_image_with_size(image_object, size)):
        render_image_with_size(image_object, size)
    # Check which filter to apply:
    image_filters = {
        Filter.GREY_SCALE: grey_scale,
        Filter.GAUSSIAN_BLUR: gaussian_blur,
    }
    image_filters[im_filter.filter_type](image_object, im_filter, size)


def convert_to_png(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    imageObject = kwargs['instance']
    filename, extension = os.path.splitext(os.path.basename(imageObject.image.name))
    img = PILImage.open(current_path_for_image(imageObject))

    if os.path.exists(path_for_image(imageObject)):
        # If there's already an image with the same name, check the checksum
        if not md5Checksum(path_for_image(imageObject)) == imageObject.checksum:
            # The images are different. Cannot rename, raise an exception
            raise ValidationError(u'There is already an image with the same name')

    #Remove old image
    os.remove(current_path_for_image(imageObject))
    img.name = path_for_image(imageObject)

    if img.format is not u'PNG' and img.format is not u'JPEG':
        #Convert image to jpg
        img.save(path_for_image(imageObject, u'.jpg'), u'JPEG', quality=80, optimize=True, progressive=True)
        #Save new path reference
        imageObject.image.name = path_for_image(imageObject, u'.jpg')
    else:
        path = path_for_image(imageObject, extension)
        img.save(path)
        imageObject.image.name = path_for_image(imageObject, extension)

    imageObject.checksum = md5Checksum(path_for_image(imageObject))
    imageObject.was_upscaled = False
    imageObject.save_bypassing_signals()

    delete_sizes_for_image(imageObject)


def get_image_on_request(image_object, size):
    if size is None:
        return media_path_for_image(image_object)
    path = path_for_image_with_size(image_object, size)

    if not os.path.exists(path) or image_object.checksum != md5Checksum(path_for_image(image_object)):
        render_image_with_size(image_object, size)
    return media_path_for_image_with_size(image_object, size)


def get_image_with_filter_and_size(image_object, im_filter, size):
    # First of all, check if it exists
    path = path_for_image_with_filter_and_size(image_object, im_filter, size)
    if not os.path.exists(path):
        render_image_with_filter_and_size(image_object, im_filter, size)
    return media_path_for_image_with_filter_and_size(image_object, im_filter, size)


def delete_images_with_size(sender, **kwargs):
    delete_images_for_size(kwargs['instance'])

def delete_images_with_filter(sender, **kwargs):
    delete_images_for_filter(kwargs['instance'])


def delete_all_sizes_of_image(sender, **kwargs):
    delete_sizes_for_image(kwargs['instance'])
    delete_filters_for_image(kwargs['instance'])


post_save.connect(convert_to_png, Image)
post_delete.connect(delete_images_with_size, Size)
post_delete.connect(delete_all_sizes_of_image, Image)
post_save.connect(delete_images_with_size, Size)
post_save.connect(delete_images_with_filter, Filter)
