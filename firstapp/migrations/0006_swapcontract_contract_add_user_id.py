# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_swapcontract_contract_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapcontract',
            name='contract_add_user_id',
            field=models.IntegerField(default=0),
        ),
    ]
