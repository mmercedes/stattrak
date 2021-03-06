# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20160418_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='isReporter',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
