# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-09 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import vip.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('subject', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=50)),
                ('bio', models.CharField(max_length=300)),
                ('guest_as', models.CharField(choices=[('JU', 'Jury'), ('LE', 'Lecturer'), ('BO', 'Jury-Lecturer')], default='JU', max_length=2)),
                ('image_path', models.ImageField(blank=True, null=True, upload_to=vip.models.directory_path)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='lecturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vip.Vip'),
        ),
    ]
