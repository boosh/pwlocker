# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Password.site_url'
        db.delete_column('passwords_password', 'site_url')

        # Adding field 'Password.url'
        db.add_column('passwords_password', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=500, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Password.site_url'
        db.add_column('passwords_password', 'site_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Deleting field 'Password.url'
        db.delete_column('passwords_password', 'url')


    models = {
        'passwords.password': {
            'Meta': {'object_name': 'Password'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['passwords']