# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-12 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csnotifier', '0002_auto_20151126_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='desc',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]