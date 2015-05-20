# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0005_auto_20150512_0926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='URL',
            new_name='url',
        ),
    ]
