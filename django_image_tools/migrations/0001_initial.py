# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=30)),
                (b'filter_type', models.PositiveSmallIntegerField(help_text='The type of filter to apply', choices=[(0, b'Grey scale')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(max_length=30)),
                (b'width', models.PositiveSmallIntegerField()),
                (b'height', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'image', models.ImageField(help_text='uploading an image will take time. DO NOT PUSH THE SAVE BUTTON AGAIN UNTIL THE IMAGE HAS BEEN SAVED!', upload_to=b'upload')),
                (b'checksum', models.CharField(max_length=32)),
                (b'filename', models.SlugField(help_text='If you want to rename the image, write here the new filename', validators=[django.core.validators.RegexValidator(regex=b'^[A-Za-z\\-\\_0-9]*$', message="Filename can only contain letters, numbers and '-'.No extensions allowed (I'll put it for you")])),
                (b'subject_position_horizontal', models.PositiveSmallIntegerField(default=2, help_text='The system will create other imagesfrom this, based on the image sizes needed.In some cases, it is necessary to cropthe image. By selecting where the subject is, the croppingcan be more accurate.', verbose_name='Subject Horizontal Position', choices=[(0, 'Left'), (1, '1/3'), (2, 'Center'), (3, '2/3'), (4, 'Right')])),
                (b'subject_position_vertical', models.PositiveSmallIntegerField(default=2, help_text='The system will create other imagesfrom this, based on the image sizes needed.In some cases, it is necessary to cropthe image. By selecting where the subject is, the croppingcan be more accurate.', verbose_name='Subject Vertical Position', choices=[(0, 'Top'), (1, '1/3'), (2, 'Center'), (3, '2/3'), (4, 'Bottom')])),
                (b'was_upscaled', models.BooleanField(default=False, verbose_name='insufficient_resolution')),
                (b'title', models.CharField(help_text='In some pages it might be necessary to display some informations.', max_length=120)),
                (b'caption', models.TextField()),
                (b'alt_text', models.CharField(help_text='This is the text that allows blind people (and google) know what the image is about ', max_length=120)),
                (b'credit', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
