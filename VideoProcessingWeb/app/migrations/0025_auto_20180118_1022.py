# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-18 02:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20171222_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='SlideVersion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 18, 2, 22, 29, 786411, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 18, 2, 22, 29, 787911, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='edittask',
            name='CreateDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]