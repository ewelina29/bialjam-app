# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-03 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_seeds_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestuserteam',
            name='message',
            field=models.TextField(),
        ),
    ]
