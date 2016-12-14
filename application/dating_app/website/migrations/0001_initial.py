# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-14 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.CharField(max_length=30)),
                ('summary', models.TextField()),
                ('age', models.IntegerField()),
                ('insertion_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
