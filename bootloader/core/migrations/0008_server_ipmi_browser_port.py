# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170320_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='ipmi_browser_port',
            field=models.IntegerField(default=80),
        ),
    ]
