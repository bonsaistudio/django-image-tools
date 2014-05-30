Testing
=======

Often times you will find yourself having images required in your models, and testing these models can be a real pain in the
donkey as you will have to create images just for that.

We want to make things simple for you, so you can import our method 'create_dummy_image' to easily create a dummy image for your tests!

::

    create_dummy_image(filename=u'Test_image', title=u'Title', caption=u'Caption', alt_text=u'Alt Text',
                       credit=u'Credit'):


This will create a new dummy entry in the database, so all you have to do is to assign it to your model's Foreign Key.

Remember to call

::

    image.delete()


In your tearDown.

Also, django_image_tools will never delete your images, so you will have to delete them yourself.
Just kidding, we made a script for that too.

::

    delete_image(image)



So, here's a complete script.

::

    def setUp(self):
        partnerImage = create_dummy_image()
        model_with_image = Model(name=u'Coca cola', image=partnerImage)
        partner.save()

    def testInsert(self):
        self.assertEqual(Model.objects.all()[0].name, 'Coca cola')

    def tearDown(self):
        model_with_image = Model.objects.all()[0]
        delete_image(model_with_image.image)
        model_with_image.delete()

Support
-------

Django Image Tools uses Travis CI to test the integration with several versions of Python and Django.
You can see the list of currently supported combinations on our `Travis CI page
<https://travis-ci.org/bonsaistudio/django-image-tools/>`_.
