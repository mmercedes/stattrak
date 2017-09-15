# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamSize', models.SmallIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('logo', models.CharField(max_length=256, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerData',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('outcome', models.CharField(max_length=1, choices=[(b'L', b'Loss'), (b'T', b'Tie'), (b'W', b'Win')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamData',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=30)),
                ('value', models.IntegerField()),
                ('result', models.ForeignKey(to='stattrak.Result')),
                ('team', models.ForeignKey(to='stattrak.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='result',
            name='awayTeam',
            field=models.ForeignKey(related_name='awayTeam', to='stattrak.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='result',
            name='homeTeam',
            field=models.ForeignKey(related_name='homeTeam', to='stattrak.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerdata',
            name='result',
            field=models.ForeignKey(to='stattrak.Result'),
            preserve_default=True,
        ),
    ]
