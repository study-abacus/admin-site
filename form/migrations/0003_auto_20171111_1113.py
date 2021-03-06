# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-11 11:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0002_auto_20171102_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=200)),
                ('score', models.FloatField()),
                ('position', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='fee',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 11, 11, 13, 49, 658855, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 11, 11, 13, 49, 656782, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='doe',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 11, 11, 13, 49, 656739, tzinfo=utc), null=True),
        ),
        migrations.AddField(
            model_name='achievement',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.Student'),
        ),
    ]
