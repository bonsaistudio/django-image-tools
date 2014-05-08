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
import hashlib
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image as PILImage
import os
from django.db.models.signals import post_save, post_init, post_delete
from . import settings


class Size(models.Model):
    name = models.CharField(max_length=30)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u'{0} - ({1}, {2})'.format(self.name, self.width, self.height)


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
                                                                  'numbers and \'-\'.'
                                                                  'No extensions allowed (I\'ll put it for you'), ]
    )
    subject_position_horizontal = models.PositiveSmallIntegerField(choices=choices_H,
                                                                   default=2,
                                                                   verbose_name=u'Subject Horizontal Position',
                                                                   help_text=u'The system will create other images'
                                                                             'from this, based on the '
                                                                             'image sizes needed.'
                                                                             'In some cases, it is necessary to crop'
                                                                             'the image. By selecting where the '
                                                                             'subject is, the cropping'
                                                                             'can be more accurate.')
    subject_position_vertical = models.PositiveSmallIntegerField(choices=choices_V,
                                                                 default=2,
                                                                 verbose_name=u'Subject Vertical Position',
                                                                 help_text=u'The system will create other images'
                                                                           'from this, based on the '
                                                                           'image sizes needed.'
                                                                           'In some cases, it is necessary to crop'
                                                                           'the image. By selecting where the '
                                                                           'subject is, the cropping'
                                                                           'can be more accurate.')
    was_upscaled = models.BooleanField(default=False, verbose_name=u'insufficient_resolution')

    title = models.CharField(max_length=120,
                             help_text=u'In some pages it might be necessary to display some informations.')
    caption = models.TextField()
    alt_text = models.CharField(max_length=120,
                                help_text=u'This is the text that allows blind people (and google) know '
                                          'what the image is about ')

    credit = models.TextField(null=True, blank=True)

    def thumbnail(self):
        if hasattr(self, u'get_thumbnail'):
            return u'<img src="{thumbnail_path}" width="100" height="100" />'.format(
                thumbnail_path=self.get_thumbnail()
            )
        else:
            return u'<img src="{thumbnail_path}" width="100" height="100" />'.format(
                thumbnail_path=self.get_original()
            )
    thumbnail.allow_tags = True

    def subject_coordinates(self):
        h = self.image.width * (self.subject_position_horizontal / float(4))
        v = self.image.height * (self.subject_position_vertical / float(4))
        return h, v

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if os.path.exists(path_for_image(self)) and md5Checksum(path_for_image(self)) != self.checksum:
            raise ValidationError('An image with the same name already exists!')
        super(Image, self).save(force_insert=force_insert,
                                force_update=force_update, using=using, update_fields=update_fields)



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

    print('Original size is ({0}, {1}), resizing to ({2}, {3})'.format(osize[0], osize[1], nsize[0], nsize[1]))

    original_ratio = original_width/original_height
    new_ratio = new_width/new_height

    print('Original ratio is {0}, new ratio is {1}'.format(original_ratio, new_ratio))

    if original_ratio < new_ratio:
        #Resize by height
        print('Considering new height as base')
        first_step_height = original_width/new_ratio
        first_step_width = original_width
        first_step_size = (first_step_width,first_step_height)
    else:
        #Resize by width
        print('Considering new Width as base')
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
        os.remove(path_for_image_with_size(image, size))


def delete_images_for_size(size):
    for image in Image.objects.all():
        delete_image_with_size(image, size)


def delete_sizes_for_image(image):
    for size in Size.objects.all():
        delete_image_with_size(image, size)


def path_for_image_with_size(image, size):
    return u'{0}/{1}/{2}'.format(settings.MEDIA_ROOT, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                 image_with_size(image, size))


def media_path_for_image(image):
    filename, extension = os.path.splitext(os.path.basename(image.image.name))
    return u'{0}{1}{2}'.format(settings.MEDIA_URL, filename, extension)


def media_path_for_image_with_size(image, size):
    return u'{0}{1}/{2}'.format(settings.MEDIA_URL, settings.DJANGO_IMAGE_TOOLS_CACHE_DIR,
                                image_with_size(image, size))


def current_path_for_image(imageObject):
    return imageObject.image.name


def path_for_image(imageObject, force_extension=None):
    filename, extension = os.path.splitext(os.path.basename(imageObject.image.name))
    if force_extension is not None:
        extension = force_extension
    return u'{0}/{1}{2}'.format(settings.MEDIA_ROOT, imageObject.filename, extension)


def image_with_size(image, size):
    filename, extension = os.path.splitext(os.path.basename(image.image.name))
    return u'{0}_{1}{2}'.format(filename, size.name, extension)


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


def convert_to_png(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    imageObject = kwargs['instance']
    filename, extension = os.path.splitext(os.path.basename(imageObject.image.name))
    img = PILImage.open(current_path_for_image(imageObject))

    if os.path.exists(path_for_image(imageObject)):
        # If there's already an image with the same name, check the checksum
        if not md5Checksum(path_for_image(imageObject)) == imageObject.checksum:
            # The images are different. Cannot rename, raise an exception
            raise ValidationError('There is already an image with the same name')

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
    path = path_for_image_with_size(image_object, size)

    if not os.path.exists(path) or image_object.checksum != md5Checksum(path_for_image(image_object)):
        render_image_with_size(image_object, size)
    return media_path_for_image_with_size(image_object, size)


def add_size_urls_to_image(sender, **kwargs):
   # the object which is saved can be accessed via kwargs 'instance' key.
    imageObject = kwargs['instance']

    # Add a way to obtain the original path

    setattr(imageObject, u'get_original', lambda: media_path_for_image(imageObject))

    for size in Size.objects.all():
        #Check if file exists
        setattr(imageObject, u'get_{0}'.format(size.name),
                (lambda x, y: lambda: get_image_on_request(x, y))(imageObject, size))


def delete_images_with_size(sender, **kwargs):
    delete_images_for_size(kwargs['instance'])


def delete_all_sizes_of_image(sender, **kwargs):
    delete_sizes_for_image(kwargs['instance'])


post_save.connect(convert_to_png, Image)
post_init.connect(add_size_urls_to_image, Image)
post_delete.connect(delete_images_with_size, Size)
post_delete.connect(delete_all_sizes_of_image, Image)
post_save.connect(delete_images_with_size, Size)
