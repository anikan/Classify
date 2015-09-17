# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteScrape', '0006_auto_20150912_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='CAPELink',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='teacher',
            name='RMPLink',
            field=models.CharField(default=b'', max_length=75),
        ),
    ]
