# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'django_image_tools', b'0003_added_numeric_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'size',
            name=b'auto',
            field=models.PositiveSmallIntegerField(default=0, help_text='Choose whether to force aspect ratio or resize based on width / height', choices=[(0, 'Force aspect ratio'), (1, 'Resize based on width'), (2, 'Resize based on height')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name=b'size',
            name=b'width',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name=b'size',
            name=b'height',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
