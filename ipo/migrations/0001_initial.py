# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-23 15:16
from __future__ import unicode_literals

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('method', models.CharField(max_length=16)),
                ('status', models.SmallIntegerField()),
                ('referrer', models.URLField()),
                ('response', models.BinaryField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='job',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='method',
            field=models.CharField(default='get', max_length=16),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
    ]
