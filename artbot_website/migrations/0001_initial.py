# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField()),
                ('venue', models.TextField()),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('image', models.TextField()),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('venue', 'title')]),
        ),
    ]
