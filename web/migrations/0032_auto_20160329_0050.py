# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0031_auto_20160329_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songalbum',
            name='infoExtra',
            field=models.TextField(blank=True, null=True, verbose_name='Informacion extra'),
        ),
    ]
