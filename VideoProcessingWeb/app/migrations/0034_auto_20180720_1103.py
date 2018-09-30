# Generated by Django 2.0.7 on 2018-07-20 03:03

import app.CustomClass.ModelsFields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20180508_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courselog',
            name='note',
        ),
        migrations.AddField(
            model_name='courselog',
            name='log',
            field=app.CustomClass.ModelsFields.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='CreateDate',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 20, 3, 3, 35, 412040, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='ExtendedData',
            field=app.CustomClass.ModelsFields.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courselog',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 20, 3, 3, 35, 414039, tzinfo=utc)),
        ),
    ]