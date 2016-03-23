# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 05:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20160323_0455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Efemeride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('event', models.TextField(verbose_name='Efemeride')),
            ],
            options={
                'verbose_name': 'Efemeride',
                'verbose_name_plural': 'Efemerides',
            },
        ),
        migrations.AlterModelOptions(
            name='biografia',
            options={'verbose_name': 'Biografia', 'verbose_name_plural': 'Biografias'},
        ),
        migrations.AddField(
            model_name='efemeride',
            name='bio',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='web.Biografia'),
        ),
    ]