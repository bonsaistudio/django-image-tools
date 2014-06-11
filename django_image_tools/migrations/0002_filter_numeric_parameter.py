# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'django_image_tools', b'0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'filter',
            name=b'numeric_parameter',
            field=models.FloatField(null=True, verbose_name='Numeric Parameter', blank=True),
            preserve_default=True,
        ),
    ]
