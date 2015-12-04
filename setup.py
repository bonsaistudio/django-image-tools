from distutils.core import setup

setup(name='django-image-tools-2',
      version='v1.0',
      description='Image tools for Django',
      author='Gabriele Platania',
      author_email='gabriele.platania@gmail.com',
      url='http://github.com/bonsaistudio/django-image-tools',
      license='BSD',
      keywords='django image filter tools resize crop',
      long_description=open('README.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
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
