# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteScrape', '0005_auto_20150912_0911'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['aggregateRating']},
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='rating',
            new_name='aggregateRating',
        ),
        migrations.AddField(
            model_name='teacher',
            name='capeRating',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
        migrations.AddField(
            model_name='teacher',
            name='rateMyProfRating',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=1),
        ),
    ]
