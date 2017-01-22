# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

# 每个任务的数据表
class SqlInjection(models.Model):
    task_id = models.CharField('任务id', max_length=1000, db_index=True)
    target_url = models.URLField(max_length=1000, unique=True)
    scan_status = models.CharField(max_length=1000)
    scan_data = models.CharField(max_length=1000)
    scan_log = models.CharField(max_length=1000)
    vulnerability = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ('-vulnerability', )

# 一次性导入的url的数据表
class UrlList(models.Model):
    target_urls = models.TextField(null=True)

# 各种配置的数据表
class ScanConfig(models.Model):
    thread_num = models.IntegerField(default=2)