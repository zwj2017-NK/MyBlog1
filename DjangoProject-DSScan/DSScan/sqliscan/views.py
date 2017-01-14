# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import SqlInjection, UrlList
from .forms import UrlListForm


# 显示所有扫描任务
def sql_tasks(request):
    # UrlList 所有对象
    url_lists = UrlList.objects.all()
    # 每个UrlList对象
    for each_list in url_lists:
        # print each_list.target_urls
        # 每个UrlList对象中的所有urls
        urls = each_list.target_urls
        # 进行字符串分割，生成一个列表，前端输入数据是以换行回车
        url_list = urls.split('\r\n')
        # print url_list
        for each_url in url_list:
            # SqlInjection.objects.values() 返回的是字典为元素的一列数据的列表，所以dic_url是字典
            dic_url = {'target_url': each_url}
            # 如果SqlInjection数据表中没有，则增加至其中
            if dic_url not in SqlInjection.objects.values("target_url"):
                # print SqlInjection.objects.values("target_url")
                SqlInjection.objects.create(target_url=each_url)

    tasks = SqlInjection.objects.all()

    return render(request, 'sqliscan/task.html', {'tasks': tasks})


# 导入扫描URL列表
def url_sql(request):

    if request.method == 'POST':
        form = UrlListForm(request.POST)
        if form.is_valid():
            # single_urls = form.cleaned_data['target_urls']
            # print single_urls
            # single_url = single_urls.split('\r\n')
            # print single_url
            # url_form = form.save(commit=False)
            # url_form.save()
            form.save()
    else:
        form = UrlListForm()

    return render(request, 'sqliscan/open.html', {'form': form})
