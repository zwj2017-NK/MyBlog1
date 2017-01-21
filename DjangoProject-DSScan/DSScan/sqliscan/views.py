# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import SqlInjection, UrlList
from .forms import UrlListForm
from .sqls import *
from Queue import Queue



# 显示所有有漏洞的任务
def vul_tasks(request):
    # 必定是扫描过的任务
    vuls = SqlInjection.objects.filter(vulnerability=True)
    # print vuls
    num_vul = len(vuls)
    return render(request, 'sqliscan/vuls.html', {'vuls': vuls, 'num_vul': num_vul})


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
        # url_list 被导入至 SqlInjection 数据表中，删除 UrlList 中的 each_list 对象
        each_list.delete()

    tasks = SqlInjection.objects.all()

    num_url = len(tasks)

    return render(request, 'sqliscan/task.html', {'tasks': tasks, 'num_url': num_url})


# 导入扫描URL列表
def url_sql(request):
    # 成功提交会跳转成功的提示
    submit = False

    if request.method == 'POST':
        form = UrlListForm(request.POST)
        if form.is_valid():
            # single_urls = form.cleaned_data['target_urls']
            #  print single_urls
            # single_url = single_urls.split('\r\n')
            # print single_url
            # url_form = form.save(commit=False)
            # url_form.save()
            form.save()
            submit = True

    else:
        form = UrlListForm()

    return render(request, 'sqliscan/open.html', {'form': form, 'submit': submit})


# 启动扫描Scan
def sql_scan(request):

    tasks = SqlInjection.objects.all()
    # 创建一个队列用于存放 target_url
    url_queue = Queue()

    # 获取复选框状态
    checkList = request.POST.getlist('checkbox')
    print checkList
    btnVal = request.POST.get('btn')
    print btnVal
    # 如果复选框选中，并且点击删除
    if checkList and btnVal == 'btnDelete':
        for urlTarget in checkList:
            # print urlTarget
            SqlInjection.objects.filter(target_url=newTarget).delete()
            # print "Deleted."

    if checkList and btnVal == 'btnScan':
        for urlTarget in checkList:
            url_queue.put(urlTarget)

        # print url_queue.queue
        # 创建一个列表，用于保存线程
        threads = []
        # 测试4个线程
        for x in xrange(4):
            threads.append(ScanThread(url_queue))
            threads[x].start()

        for y in threads:
            y.join()

    return render(request, 'sqliscan/scan.html', {'tasks': tasks})

