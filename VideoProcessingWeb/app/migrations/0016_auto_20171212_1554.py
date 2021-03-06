# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-12 07:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20171206_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edittask',
            name='AudioExtractDate',
        ),
        migrations.AddField(
            model_name='course',
            name='ProjectId',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='SourceCourseId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='note',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 12, 7, 54, 53, 197757, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 12, 7, 54, 53, 197757, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='edittask',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 12, 7, 54, 53, 197757, tzinfo=utc)),
        ),
    ]
