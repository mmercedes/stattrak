# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20160324_0355'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\d{10}$', message=b"Phone number must be entered in the format: '0123456789'")]),
            preserve_default=True,
        ),
    ]
