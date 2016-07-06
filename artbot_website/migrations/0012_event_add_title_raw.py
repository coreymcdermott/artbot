# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_title_raw(apps, schema_editor):
    # We can't import the Event model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Event = apps.get_model("artbot_website", "Event")
    for event in Event.objects.all():
        event.title_raw = event.titleRaw
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0011_auto_20160605_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title_raw',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(migrate_title_raw),
    ]
