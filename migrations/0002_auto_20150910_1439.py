# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteScrape', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='averageGrade',
            field=models.CharField(default=b'', max_length=3),
        ),
        migrations.AddField(
            model_name='teacher',
            name='responseRate',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='quarters',
            field=models.IntegerField(default=0),
        ),
    ]
