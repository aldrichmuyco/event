# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-17 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pageant', '0002_pageantparticipant_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageantparticipant',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
