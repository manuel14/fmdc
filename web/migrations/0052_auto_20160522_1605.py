# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-22 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0051_actividadimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='link',
            field=models.FileField(default='', upload_to='videos/', verbose_name='Video'),
        ),
    ]