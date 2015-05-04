# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0003_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='is_valid',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
