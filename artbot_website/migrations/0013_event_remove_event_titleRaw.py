# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0012_event_add_title_raw'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('venue', 'title_raw')]),
        ),
        migrations.RemoveField(
            model_name='event',
            name='titleRaw',
        ),
    ]
