# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='serial',
            field=models.CharField(max_length=255, null=True),
        ),
    ]