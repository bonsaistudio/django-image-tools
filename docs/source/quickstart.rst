Quick Start
===========

All you have to do is

::

    pip install django-image-tools

and of course, add the app in your INSTALLED_APPS as

::

    INSTALLED_APPS = (
        ...
        'django_image_tools',
        ...
    )

Configuration
-------------

The minimum required settings you should add in your settings.py are:

::

    # Folder in which you want to store your images, in this example it's the sub folder 'media'
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    # Temporary folder for upload, in this example is the subfolder 'upload'
    UPLOAD_TO = os.path.join(PROJECT_ROOT, 'media/upload')

The folders will be created if they do not exist.

You should also add your filters and sizes in your settings file, like this:

::

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


That's it, you're good to go now.
Let's create a couple of models containing images!


Example models
--------------

Let's say you have a "Person" model and you want to include an Avatar, or a profile pic. Here's how you do it

::

    ....
    from django_image_tools.models import Image

    class Person(models.Model):

        first_name = models.CharField(max_length=255)
        second_name = models.CharField(max_length=255)
        ...

        picture = models.ForeignKey(Image)



You can also (obviously) use a ManyToMany field, for example:

::

    ....
    from django_image_tools.models import Image

    class Slideshow(models.Model):
       title = models.CharField(max_length=255)
       description = models.TextField()
       ...

       slides = models.ManyToManyField(Image)



That's all you need to do when dealing with the models.

Then, in your templates, you can use them like this:

::

    # Displaying a thumbnail
    <img src={{ person.image.get__thumbnail }} />

    # Displaying a blurred thumbnail
    <img src={{ person.image.get__blurred__thumbnail }} />

    # Displaying the original image
    <img src={{ person.image.get__original }} />

    # Displaying the blurred (original) image
    <img src={{ person.image.get__blurred__original }} />


Including thumbnails in your admin
----------------------------------

You can include thumbnail in your admin panel

Just look at this admin.py file

::

    from __future__ import absolute_import
    from django.contrib import admin
    from .models import Person


    class PersonAdmin(admin.ModelAdmin):
        list_display = ('thumbnail', 'first_name', 'second_name')

    admin.site.register(Person, PersonAdmin)


You will also need to tweak your model so that it uses the ``thumbnail`` method of the correct image.
Here's an example:

::

    from django.db import models
    from django_image_tools.models import Image


    class Person(models.Model):
        first_name = models.CharField(max_length=255)
        second_name = models.CharField(max_length=255)

        picture = models.ForeignKey(Image)

        # Add the thumbnail method and grab the image thumbnail
        def thumbnail(self):
            return self.picture.thumbnail()

        # Now you only need to tell django that this thumbnail field is safe
        thumbnail.allow_tags = True


Please note that in this case we used the ``picture.thumbnail()`` method, and not the ``picture.get__thumbnail``
because this particular method is designed to output the whole 'img' tag for the django admin panel.

If you have any problem, make sure you followed `Django's guide to serve static and user uploaded files
<https://docs.djangoproject.com/en/1.6/howto/static-files/>`_ !

