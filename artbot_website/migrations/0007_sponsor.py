# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0006_auto_20160314_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.TextField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
    ]
