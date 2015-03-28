# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150327_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthybee',
            name='lastSyncTime',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
