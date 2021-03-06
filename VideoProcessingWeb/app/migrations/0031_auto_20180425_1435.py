# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-25 06:35
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0030_auto_20180419_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='SegmentTime',
            new_name='ExtendedData',
        ),
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='edittask',
            name='ExtendedData',
            field=models.CharField(max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name='edittask',
            name='creator',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 6, 35, 26, 145324, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 6, 35, 26, 145324, tzinfo=utc)),
        ),
    ]
