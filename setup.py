from distutils.core import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-image-tools',
      version='0.6.b5',
      description='Image tools for Django',
      author='Bonsai Studio',
      author_email='info@bonsai-studio.net',
      url='http://github.com/bonsaistudio/django-image-tools',
      license='BSD',
      keywords='django image filter tools resize crop',
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Django',
          'Environment :: Web Environment',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
      ],
      packages=['django_image_tools', 'django_image_tools.migrations'],
      )
