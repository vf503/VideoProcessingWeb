# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-14 04:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170614_0800'),
    ]

    operations = [
        migrations.RenameField(
            model_name='edittask',
            old_name='CourseId',
            new_name='course',
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 4, 46, 42, 669750, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='edittask',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 14, 4, 46, 42, 685374, tzinfo=utc)),
        ),
    ]
