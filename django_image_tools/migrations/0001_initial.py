# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Size'
        db.create_table(u'django_image_tools_size', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('auto', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'django_image_tools', ['Size'])

        # Adding model 'Filter'
        db.create_table(u'django_image_tools_filter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('filter_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('numeric_parameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_image_tools', ['Filter'])

        # Adding model 'Image'
        db.create_table(u'django_image_tools_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('filename', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('subject_position_horizontal', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('subject_position_vertical', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('was_upscaled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('alt_text', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('credit', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_image_tools', ['Image'])


    def backwards(self, orm):
        # Deleting model 'Size'
        db.delete_table(u'django_image_tools_size')

        # Deleting model 'Filter'
        db.delete_table(u'django_image_tools_filter')

        # Deleting model 'Image'
        db.delete_table(u'django_image_tools_image')


    models = {
        u'django_image_tools.filter': {
            'Meta': {'object_name': 'Filter'},
            'filter_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'numeric_parameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'django_image_tools.image': {
            'Meta': {'object_name': 'Image'},
            'alt_text': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'caption': ('django.db.models.fields.TextField', [], {}),
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'credit': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'subject_position_horizontal': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'subject_position_vertical': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'was_upscaled': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'django_image_tools.size': {
            'Meta': {'object_name': 'Size'},
            'auto': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_image_tools']