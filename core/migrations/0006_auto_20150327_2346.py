# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_healthdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthdata',
            name='bee',
            field=models.ForeignKey(to='core.HealthyBee', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='dataTypeName',
            field=models.CharField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='endTime',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='intVal',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='modifiedTime',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='originalDataSourceId',
            field=models.CharField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='startTime',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
