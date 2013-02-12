# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Test'
        db.create_table('datedge_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text1', self.gf('django.db.models.fields.TextField')()),
            ('text2', self.gf('django.db.models.fields.TextField')()),
            ('text3', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('datedge', ['Test'])

        # Adding model 'Question'
        db.create_table('datedge_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datedge.Test'])),
            ('text_idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('option1', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('option2', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('option3', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('option4', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('option5', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('answer_idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('datedge', ['Question'])

        # Adding model 'Sitting'
        db.create_table('datedge_sitting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datedge.Test'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('datedge', ['Sitting'])

        # Adding model 'Answer'
        db.create_table('datedge_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sitting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datedge.Sitting'])),
            ('answer_idx', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('datedge', ['Answer'])

        # Adding M2M table for field question on 'Answer'
        db.create_table('datedge_answer_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answer', models.ForeignKey(orm['datedge.answer'], null=False)),
            ('question', models.ForeignKey(orm['datedge.question'], null=False))
        ))
        db.create_unique('datedge_answer_question', ['answer_id', 'question_id'])

        # Adding model 'Activation'
        db.create_table('datedge_activation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('expiry', self.gf('django.db.models.fields.DateField')()),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('datedge', ['Activation'])

        # Adding model 'Scaling'
        db.create_table('datedge_scaling', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('min_score', self.gf('django.db.models.fields.IntegerField')()),
            ('max_score', self.gf('django.db.models.fields.IntegerField')()),
            ('scaled', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('datedge', ['Scaling'])


    def backwards(self, orm):
        # Deleting model 'Test'
        db.delete_table('datedge_test')

        # Deleting model 'Question'
        db.delete_table('datedge_question')

        # Deleting model 'Sitting'
        db.delete_table('datedge_sitting')

        # Deleting model 'Answer'
        db.delete_table('datedge_answer')

        # Removing M2M table for field question on 'Answer'
        db.delete_table('datedge_answer_question')

        # Deleting model 'Activation'
        db.delete_table('datedge_activation')

        # Deleting model 'Scaling'
        db.delete_table('datedge_scaling')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datedge.activation': {
            'Meta': {'object_name': 'Activation'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'datedge.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datedge.Question']", 'symmetrical': 'False'}),
            'sitting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datedge.Sitting']"})
        },
        'datedge.question': {
            'Meta': {'object_name': 'Question'},
            'answer_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option1': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'option2': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'option3': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'option4': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'option5': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datedge.Test']"}),
            'text_idx': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'datedge.scaling': {
            'Meta': {'object_name': 'Scaling'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {}),
            'min_score': ('django.db.models.fields.IntegerField', [], {}),
            'scaled': ('django.db.models.fields.IntegerField', [], {})
        },
        'datedge.sitting': {
            'Meta': {'object_name': 'Sitting'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datedge.Test']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'datedge.test': {
            'Meta': {'object_name': 'Test'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text1': ('django.db.models.fields.TextField', [], {}),
            'text2': ('django.db.models.fields.TextField', [], {}),
            'text3': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['datedge']