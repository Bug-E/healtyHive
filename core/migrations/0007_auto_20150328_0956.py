# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150327_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeeCoupons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bee', models.ForeignKey(to='core.HealthyBee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HealthCoupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='HealthyHive',
        ),
        migrations.AddField(
            model_name='beecoupons',
            name='coupon',
            field=models.ForeignKey(to='core.HealthCoupon'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='healthdata',
            name='intVal',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
