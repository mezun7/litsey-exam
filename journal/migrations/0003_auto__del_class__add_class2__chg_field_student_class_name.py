# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Class'
        db.delete_table(u'journal_class')

        # Removing M2M table for field teacher on 'Class'
        db.delete_table(db.shorten_name(u'journal_class_teacher'))

        # Adding model 'Class2'
        db.create_table(u'journal_class2', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parallel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journal.Parallel'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('class1_teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'journal', ['Class2'])

        # Adding M2M table for field teacher on 'Class2'
        m2m_table_name = db.shorten_name(u'journal_class2_teacher')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class2', models.ForeignKey(orm[u'journal.class2'], null=False)),
            ('teacher', models.ForeignKey(orm[u'journal.teacher'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class2_id', 'teacher_id'])


        # Changing field 'Student.class_name'
        db.alter_column(u'journal_student', 'class_name_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journal.Class2'], null=True))

    def backwards(self, orm):
        # Adding model 'Class'
        db.create_table(u'journal_class', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('class1_teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parallel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journal.Parallel'])),
        ))
        db.send_create_signal(u'journal', ['Class'])

        # Adding M2M table for field teacher on 'Class'
        m2m_table_name = db.shorten_name(u'journal_class_teacher')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'journal.class'], null=False)),
            ('teacher', models.ForeignKey(orm[u'journal.teacher'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'teacher_id'])

        # Deleting model 'Class2'
        db.delete_table(u'journal_class2')

        # Removing M2M table for field teacher on 'Class2'
        db.delete_table(db.shorten_name(u'journal_class2_teacher'))


        # Changing field 'Student.class_name'
        db.alter_column(u'journal_student', 'class_name_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journal.Class'], null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'journal.class2': {
            'Meta': {'object_name': 'Class2'},
            'class1_teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'parallel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Parallel']"}),
            'teacher': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.Teacher']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'journal.mark': {
            'Meta': {'object_name': 'Mark'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.FloatField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Student']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Teacher']"})
        },
        u'journal.markscoeff': {
            'Meta': {'object_name': 'MarksCoeff'},
            'coeff': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Subject']"})
        },
        u'journal.parallel': {
            'Meta': {'object_name': 'Parallel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['journal.Subject']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'journal.student': {
            'Meta': {'object_name': 'Student'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'class_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Class2']", 'null': 'True', 'blank': 'True'}),
            'fathers_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'medical_card': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_for_eating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'phone_parent': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'report_from_school': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'journal.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'journal.teacher': {
            'Meta': {'object_name': 'Teacher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['journal.Subject']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['journal']