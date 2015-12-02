More features
=============

The images will all be available in the admin panel. You can browse and search through all of them.
Sometimes, the users will upload a 'small' image (You know users right?) and then they'll complain that the image
doesn't scale well, or it's too jpegged.
The app will automatically flag all images for which an upscaled version was requested, by flagging them with the
'was_upscaled' flag (if you're using django_suit, the background of the row will also be displayed red). You can use
 the filter in the app to see which one were upscaled, and delete them, or replace them with a higher-res version.
The original images will never be touched, unless the user wants to rename them.
The cached image folder can be changed in the system settings, through the settings variable
'DJANGO_IMAGE_TOOLS_CACHE_DIR'. This will always be a sub dir of the 'MEDIA' dir, though I might change this
in the future.
I strongly advice you to use the 'raw_id_fields' for the image fields, as it will allow the user to search for a
previously submitted image or input a new one with a nice popup menu. This will decrease the number of duplicates.
If there is a 'thumbnail' size, the app will display images of that size for the admin panel, otherwise it will fall
back on the original.
You can fetch the original image path by requesting 'image.get__original'.