from distutils.core import setup

setup(name='django-image-tools',
      version='0.8.b1',
      description='Image tools for Django',
      author='Bonsai Studio',
      author_email='info@bonsai-studio.net',
      url='http://github.com/bonsaistudio/django-image-tools',
      license='BSD',
      keywords='django image filter tools resize crop',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Framework :: Django',
          'Environment :: Web Environment',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
      ],
      install_requires=[
          'Pillow',
      ],
      packages=['django_image_tools', 'django_image_tools.migrations'],
      )
