# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0004_auto_20160226_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.TextField()),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name=b'timestamp')),
            ],
        ),
    ]