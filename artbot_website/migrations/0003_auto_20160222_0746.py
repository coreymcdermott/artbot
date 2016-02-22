# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0002_auto_20160109_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='titleRaw',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.TextField(),
        ),
        migrations.RunSQL(
            "UPDATE artbot_website_event SET titleRaw = title;"
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('venue', 'titleRaw')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='titleRaw',
            field=models.TextField(),
        ),
    ]
