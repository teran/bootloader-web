# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 18:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0012_auto_20170418_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logentry',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-created']},
        ),
    ]
