# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0006_auto_20150520_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopStories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('date_published', models.DateField()),
                ('section', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('abstract', models.TextField()),
                ('location', models.ForeignKey(to='visualizer.Location')),
            ],
        ),
    ]
