# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_swapintermediate'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapcontract',
            name='contract_accept',
            field=models.IntegerField(default=0),
        ),
    ]