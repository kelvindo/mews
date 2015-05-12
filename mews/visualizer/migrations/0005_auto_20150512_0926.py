# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0004_location_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_published',
            field=models.DateField(default=datetime.datetime(2015, 5, 12, 9, 26, 5, 187121, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='location',
            field=models.ForeignKey(default=0, to='visualizer.Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='section',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
