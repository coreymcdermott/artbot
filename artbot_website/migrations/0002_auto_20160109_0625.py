# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artbot_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.TextField(unique=True),
        ),
    ]
