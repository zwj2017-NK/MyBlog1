# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import SqlInjection

# 显示所有扫描任务
def sql_tasks(request):
    tasks = SqlInjection.objects.all()
    return render(request, 'sqliscan/task.html', {'tasks': tasks})
