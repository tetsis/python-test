# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170311_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
    ]