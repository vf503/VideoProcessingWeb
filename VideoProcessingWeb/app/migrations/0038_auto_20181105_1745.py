# Generated by Django 2.0.7 on 2018-11-05 09:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20181101_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 5, 9, 45, 32, 881198, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 5, 9, 45, 32, 883196, tzinfo=utc)),
        ),
    ]
