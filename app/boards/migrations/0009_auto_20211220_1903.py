# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-20 19:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_auto_20211220_1901'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='details',
            new_name='pd',
        ),
    ]
