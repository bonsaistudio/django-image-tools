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


That's it, you're good to go now.

Login to your admin panel and check out the options!

