# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 11:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firstapp', '0003_auto_20170716_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwapIntermediate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swap_name_temp', models.CharField(max_length=100)),
                ('swap_type_temp', models.CharField(max_length=100)),
                ('margin_money_temp', models.IntegerField()),
                ('user_temp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]