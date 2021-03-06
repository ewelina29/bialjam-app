# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 22:55
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def load_information_from_fixture(apps, schema_editor):
    call_command("loaddata", "information")


def delete_information(apps, schema_editor):
    info = apps.get_model('information', 'Information')
    info.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('information', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_information_from_fixture, delete_information),
    ]
