# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 22:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0011_auto_20170428_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='ipmi_password',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ipmi_username',
        ),
    ]
