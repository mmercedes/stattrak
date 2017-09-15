# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_account_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pic',
            field=models.CharField(default=b'/static/img/profile.png', max_length=256, blank=True),
            preserve_default=True,
        ),
    ]
