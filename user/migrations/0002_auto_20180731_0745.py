# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-31 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plt_icon',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=18),
        ),
    ]
