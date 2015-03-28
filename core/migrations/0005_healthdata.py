# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_healthybee_lastsynctime'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.IntegerField()),
                ('endTime', models.IntegerField()),
                ('dataTypeName', models.CharField(max_length=256)),
                ('originalDataSourceId', models.CharField(max_length=256)),
                ('intVal', models.IntegerField()),
                ('modifiedTime', models.IntegerField()),
                ('bee', models.ForeignKey(to='core.HealthyBee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
