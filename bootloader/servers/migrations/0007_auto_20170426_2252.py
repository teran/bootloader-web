# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0006_auto_20170426_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='ipmi_browser_proto',
            field=models.CharField(choices=[('http', 'http'), ('https', 'https')], default='http', max_length=5),
            preserve_default=False,
        ),
    ]
