# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 19:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0008_auto_20170704_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fee',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 4, 19, 5, 56, 816945, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(default=datetime.datetime(2017, 7, 4, 19, 5, 56, 789074, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='doe',
            field=models.DateField(default=datetime.datetime(2017, 7, 4, 19, 5, 56, 788959, tzinfo=utc), null=True),
        ),
    ]
