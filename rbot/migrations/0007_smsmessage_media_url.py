# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbot', '0006_auto_20170325_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsmessage',
            name='media_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]