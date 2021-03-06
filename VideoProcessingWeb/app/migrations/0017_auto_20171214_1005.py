# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 02:05
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20171212_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAbstract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(validators=[django.core.validators.MaxValueValidator(50)])),
                ('Text', models.CharField(max_length=2048, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='AbstractText',
        ),
        migrations.AddField(
            model_name='course',
            name='FilePath',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 5, 21, 273499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 5, 21, 273499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='edittask',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 5, 21, 273499, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='courseabstract',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course'),
        ),
        migrations.AlterUniqueTogether(
            name='courseabstract',
            unique_together=set([('course', 'index')]),
        ),
    ]
