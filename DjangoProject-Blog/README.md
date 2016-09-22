# DjangoProject-Blog

## Project process
* django-admin startproject mysite 创建项目
* cd mysite
* python manage.py migrate 创建数据库
* python manage.py runserver (python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings) 试运行
* python manage.py startapp blog 创建应用
* models.py
  * 添加`Post`模型
  ```Python
  from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish', )

    def _str_(self):
        return self.title
  ```

### Instruction
