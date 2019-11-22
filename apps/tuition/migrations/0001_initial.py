# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-21 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('course_name', models.CharField(max_length=255)),
                ('cost', models.IntegerField()),
                ('other_fees', models.IntegerField(default=0, null=True)),
                ('total_cost', models.IntegerField(null=True)),
                ('add_info', models.TextField(blank=True, null=True)),
                ('file', models.ImageField(blank=True, null=True, upload_to='tuition.ApplicationFile/bytes/filename/mimetype')),
                ('is_pending', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('add_info_required', models.BooleanField(default=False)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='login.User')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
    ]