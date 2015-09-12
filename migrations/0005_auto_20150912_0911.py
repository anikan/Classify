# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteScrape', '0004_auto_20150910_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='rating',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='responseRate',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
    ]
