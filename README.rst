==================
Django Image Tools
==================

Django Image Tools is a small app that will allow you to manage your project's images without worrying much about image sizes, how to crop them, etc..
All you have to do is to define your website sizes and the app will do the rest for you.

============
Installation
============

All you have to do is 

    pip install django-image-tools

and of course, install in your INSTALLED_APPS as

    django_image_tools

It requires Pillow==2.1.0 to run correctly, and of course Django. Versions from 1.5 up to 1.7 have been tested successfully.

=============
Configuration
=============

The required settings you should add in your settings.py are:

    UPLOAD_TO # Temporary upload directory

    MEDIA_URL # Media path for url files
    
    MEDIA_ROOT # Absolute path to media directory

If you want to specify a different directory just for django-image-tools, you can do so by defining

    DJANGO_IMAGE_TOOLS_UPLOAD_DIR

You can also configure the app to use a specific cache dir by defining

    DJANGO_IMAGE_TOOLS_CACHE_DIR

otherwise, the cached images will be put under a 'cache' directory.



=============
How to use it
=============

You will find in the admin panel the 'django_image_tools' option. You can enter all the sizes you're going to use in your website there.
The options for each size are:

- Name
- Width  (auto)
- Height (auto)

All of the sizes you create will be available for the images the user will upload through its name.
For example, you can have a 'thumbnail' 250x250 size, and every image you upload will have the 'get_thumbnail' method that will output the path for the image with the requested size.

Having 'auto' height, for exmaple, means that the image will be resized to match the given width, and keep the original aspect ratio (This is useful for example, if you want to create a *pinterest* board).

Of course, you can only have auto height or auto width, and not both.

In the template, to display an image field, all you have to do is:

    <img src='{{ some_image.get_thumbnail }}' alt_text='{{ some_image.alt_text }}' />


Here's a list of all the fields for each image:

- checksum: A md5 checksum of the image. Useful for checking the integrity of the files with the database.
- filename: The current file name. Changing this will result in renaming the actual file (useful for SEO purposes).
        **Attempting to rename with the name of an existing file will throw an exception**
- subject_horizontal_position: The horizontal position of the subject. This is currently one of the list (left, 1/3, center, 2/3, right).
- subject_vertical_position: The vertical position of the subject. This is currently one of the list (top, 1/3, center, 2/3, bottom).
        ** If the aspect ratio of the resized image doesn't match the original ratio, the image will be cropped around this point **
- was_upscaled: flag that notices if the image was used somewhere with a size bigger than its own (resulting in an upscaling). Useful for letting the user know that it should replace this image with a higher-resolution version.
- title: A title field for the image
- caption: Caption of the image
- alt_text: for blind people and SEO
- credit: Credit field


============
How it works
============

The app only creates the image the first time it is requested. So don't worry about the system clogging because you have 10.0000 images and you create a new size on the fly, or having your server filled up with cached images that are never used.
The images are also cached, so you should never experience a notable lag, unless you request a bunch of images of a size that was never processed.

The app uses an md5 checksum to check if the image was changed. This way, it can detect even if the image was replaced by some other app, (or the user) and reprocess the various sizes of that image on request.

=============
More features
=============

The images will all be available in the admin panel. You can browse and search through all of them. 
Sometimes, the users will upload a 'small' image (You know users right?) and then they'll complain that the image doesn't scale well, or it's too jpegged. 
The app will automatically flag all images for which an upscaled version was requested, by flagging them with the 'was_upscaled' flag (if you're using django_suit, the background of the row will also be displayed red). You can use the filter in the app to see which one were upscaled, and delete them, or replace them with a higher-res version.

The original images will never be touched.

The cached image folder can be changed in the system settings, through the settings variable 'DJANGO_IMAGE_TOOLS_CACHE_DIR'. This will always be a sub dir of the 'MEDIA' dir, though I might change this in the future.

I strongly advice you to use the 'raw_id_fields' for the image fields, as it will allow the user to search for a previously submitted image or input a new one with a nice popup menu. This will decrease the number of duplicates.

I also *strongly* advice you to remove permission for non admin users for the 'size' app, as removing a size that is used inside a template will result (obviously) in a 500 error.

If there is a 'thumbnail' size, the app will display images of that size for the admin panel, otherwise it will fall back on the original.

You can fetch the original image path by requesting 'image.get_original'.
