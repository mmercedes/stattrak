# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20160325_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='rating',
            field=models.PositiveSmallIntegerField(default=500),
            preserve_default=True,
        ),
    ]
