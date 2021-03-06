# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 04:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediahistory',
            options={'verbose_name': 'Media File History', 'verbose_name_plural': 'Media File Histories'},
        ),
        migrations.AlterField(
            model_name='mediahistory',
            name='media_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='main.Media'),
        ),
    ]
