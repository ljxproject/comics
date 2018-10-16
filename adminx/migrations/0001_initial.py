# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 02:01
from __future__ import unicode_literals

import api.models.self_model
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='公告名')),
                ('file', models.FileField(upload_to='uploads/notices', verbose_name='公告文档')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '公告信息',
            },
            bases=(models.Model, api.models.self_model.Model),
        ),
        migrations.CreateModel(
            name='DataBackup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='备份文件名')),
                ('backup_type',
                 models.IntegerField(choices=[(0, '完全备份'), (1, '差异备份'), (2, '增量备份')], verbose_name='备份类型')),
                ('backup_file', models.CharField(max_length=128, verbose_name='备份文件路径')),
                ('size', models.CharField(max_length=16, verbose_name="备份文件大小")),
                ('comment', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('base', models.IntegerField(null=True, blank=True, verbose_name='父备份ID')),
            ],
            options={
                'verbose_name_plural': '恢复与备份',
            },
            bases=(models.Model, api.models.self_model.Model),
        ),
        migrations.CreateModel(
            name='MangaUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name="文件名")),
                ('resources_file', models.CharField(max_length=128, verbose_name="资源路径")),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
            ],
            options={
                'verbose_name_plural': '漫画上传',
            },
            bases=(models.Model, api.models.self_model.Model),
        ),
    ]
