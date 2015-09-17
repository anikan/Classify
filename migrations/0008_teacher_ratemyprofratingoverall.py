# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteScrape', '0007_auto_20150915_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='rateMyProfRatingOverall',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=1),
        ),
    ]
