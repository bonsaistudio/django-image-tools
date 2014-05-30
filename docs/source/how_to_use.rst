How to use it
=============

Philosophy
----------

There are many tools suitable for cutting, cropping, resizing and applying filters at runtime.
but we noticed that many of these lacked a sense of 'DRY-ness'
as almost all of them forced you to input the size and the filter options in the template itself.

Now, try to see this from a designer point of view. As a designer, I want all of the images in this template to have a
specific effect, and maybe I want a different effect for the hover version. So what do I do? Do I write down the
effect's parameters for each image in the template?

And what if I wanted to change the effect after the template is ready?

The same thing applies for image sizes, what if you suddenly needed your images to be bigger or smaller?

Django Image Tools allows you to create specific filters and sizes for your images, and bind those filters to
your images through their name, so you can change the filter parameters and the image size from the admin panel itself,
and those changes will automatically be applied to all of the bound images in your templates. Now your templates
will remain untouched even if you decide to change a filter, or even the size of your images.

We believe this will save some time looking at the docs of an app trying to figure out which custom filter file you
should include, how to input your parameters, etc...


Include it in your models
-------------------------

Nothing more simple. Just import the 'Image' model in your models.py file and create a Foreign Key to it. Done!

Syntax
------

We tried to make the syntax as readable and intuitive as possible.
Filter names should be applied before size names. Size names are mandatory.

To activate django_image_tools, you need to call a ``get__`` attribute on the image.

For example, if you want the path for a size named 'thumbnail', you should define a new Size called 'thumbnail' on
the admin panel. Then, in your templates you should use:

::

    <img src="image.get__thumbnail" />

To improve readability of your templates, we advice you to name the filters as adjectives.
For example, a Gaussian Blur could be called 'blurred'.

If you want to have a thumbnail with your Gaussian blur, now the template reads:

::

    <img src="image.get__blurred__thumbnail" />

How intuitive is that?
Note that filters and sizes are separated by a double '_', as django-esque as possible.

Obviously, you cannot add filters / sizes whose name contains a double '_'.


Size & Cropping
---------------

You will find in the admin panel the 'django_image_tools' option. You can enter all the sizes
you're going to use in your website there.
The options for each size are:

- Name
- Width  (auto)
- Height (auto)

All of the sizes you create will be available for the images the user will upload through its name.
For example, you can have a 'thumbnail' 250x250 size, and every image you upload will have the ``get__thumbnail``
method that will output the path for the image with the requested size.

Having 'auto' height, for exmaple, means that the image will be resized to match the given width, and keep the original
aspect ratio (This is useful for example, if you want to create a *pinterest* board).

Of course, you can only have auto height or auto width, but not both.

In the template, to display an image field, all you have to do is:

::

    <img src='{{ some_image.get__thumbnail }}' alt_text='{{ some_image.alt_text }}' />


Here's a list of all the fields for each image:

- checksum
    A md5 checksum of the image. Useful for checking the integrity of the files with the database.
- filename
    The current file name. Changing this will result in renaming the actual file (useful for SEO purposes).

    **Attempting to rename with the name of an existing file will throw an exception**

- subject_horizontal_position
    The horizontal position of the subject. This is currently one of the list
    (left, 1/3, center, 2/3, right).
- subject_vertical_position
    The vertical position of the subject. This is currently one of the list
    (top, 1/3, center, 2/3, bottom).

    **If the aspect ratio of the resized image doesn't match the original ratio,
    the image will be cropped around this point**

- was_upscaled
    Flag that notices if the image was used somewhere with a size
    bigger than its own (resulting in an upscaling). Useful for letting the user know that it
    should replace this image with a higher-resolution version.
- title
    A title field for the image
- caption
    Caption of the image
- alt_text
    For blind people and SEO
- credit
    Credit field


Filters
-------

Django Image tools also works great for applying filters to your images.
To define a filter, just add it in the admin panel, and tweak it with its parameters until you get the desired effect.

For example, let's say you defined a filter named 'blurred' with a Gaussian Blur and you want
a blurred thumbnail of your image.
This should be the image tag.

::

    <img src="{{ some_image.get__blurred__thumbnail }}" />


**Note** that when using a filter, the image size is mandatory. If you want to apply a filter to an image with its
original size, use 'original' as size

::

    <img src="{{ some_image.get__blurred__original }}" />

