# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 02:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20171214_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 28, 10, 257484, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 28, 10, 257484, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='edittask',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 2, 28, 10, 273110, tzinfo=utc)),
        ),
    ]
