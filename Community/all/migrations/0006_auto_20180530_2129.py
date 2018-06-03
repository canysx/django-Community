# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-30 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0005_topic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.ImageField(default='image/default.png', max_length=50, upload_to='image/topic/%Y/%m', verbose_name='封面图'),
        ),
    ]