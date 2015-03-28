# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_healthybeeauth'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthyHive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='healthybeeauth',
            name='refresh_token',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
