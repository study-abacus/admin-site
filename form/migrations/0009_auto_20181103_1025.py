# Generated by Django 2.1.2 on 2018-11-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0008_auto_20181103_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ci',
            name='center_address',
            field=models.TextField(null=True),
        ),
    ]