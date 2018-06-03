# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-20 02:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]