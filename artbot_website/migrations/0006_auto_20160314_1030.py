# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0005_auto_20160229_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='titleRaw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
