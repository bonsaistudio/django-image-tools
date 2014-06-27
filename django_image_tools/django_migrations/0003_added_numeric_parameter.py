# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'django_image_tools', b'0002_filter_numeric_parameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'filter',
            name=b'filter_type',
            field=models.PositiveSmallIntegerField(help_text='The type of filter to apply', choices=[(0, b'Grey scale'), (1, b'Gaussian Blur')]),
        ),
    ]
