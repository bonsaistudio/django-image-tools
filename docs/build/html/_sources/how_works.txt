How it works
============

The app only creates the image the first time it is requested. So don't worry about the system clogging
because you have 10.0000 images and you create a new size on the fly, or having your server filled up with cached
images that are never used.
The images are also cached, so you should never experience a notable lag, unless you request a bunch of images
of a size that was never processed.
The app uses an md5 checksum to check if the image was changed. This way, it can detect even if the image was
replaced by some other app, (or the user) and reprocess the various sizes of that image on request.