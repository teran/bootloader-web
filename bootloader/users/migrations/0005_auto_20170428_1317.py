# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170428_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshauthorizedkey',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]