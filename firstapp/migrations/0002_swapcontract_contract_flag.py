# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapcontract',
            name='contract_flag',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]