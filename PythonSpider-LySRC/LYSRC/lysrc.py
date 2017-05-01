#!/usr/bin/env python
# coding=utf-8

"""
Function: LYSRC Public Vulnerability
Author:   Pyx
Time:     2017年5月1日 09:37:06
"""

import requests
from bs4 import BeautifulSoup
import random, re, time, os
import urllib, urllib2
from Queue import Queue
from threading import Thread
from cmdline import parse_args


# 获取 url 响应
def url_resp(url):
    user_agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
    # 随机用户代理
    header = {'User-Agent': random.choice(user_agent)}
    # https 证书验证
    resp = requests.get(url, verify=False, headers=header)
    return resp


# 分析，获取 vul 链接
def url_soup(url):
    # 漏洞列表
    # global vul
    soup = BeautifulSoup(url_resp(url).content, 'html.parser', from_encoding='UTF-8')
    # 包含所有漏洞名的列表
    _soup = soup.find_all(href=re.compile('bugdetail'))
    # print _soup
    for each in _soup:
        each_url = 'http://sec.ly.com/' + each.get('href')
        print each.get('href')
        print each.div.string
        # vul.append(each.get('href'))
        vul_queue.put(each_url)
        save_result(each.get('href'))
        save_result(each.div.string.encode('utf-8'))
    # print len(vul)


# 获取漏洞列表多线程
class VulListThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            if page_queue.empty(): break
            vul_page = page_queue.get()
            url_soup(vul_page)
            page_queue.task_done()


# 保存
def save_result(vul):
    report_name = 'LYSRC' + time.strftime('%Y%m%d', time.localtime()) + '.txt'
    with open(report_name, 'a+') as f:
        f.write(vul)
        f.write('\n')


# vul 详情页面
def vul_detail(url):
    vul_soup = BeautifulSoup(url_resp(url).content, 'html.parser', from_encoding='UTF-8')
    _vul_soup = vul_soup.find_all('img')
    # print _vul_soup
    # 保存图片 url 列表
    img_list = []
    # 有些标题中有 \ 等符号，一次性全部正则替换
    title = re.sub(r'[/\?\\<>:\*]', '', vul_soup.find('h2').string)
    # print title.string

    # 创建目录，同目录下
    vul_path = './' + title
    if os.path.exists(vul_path):
        pass
    else:
        os.makedirs(vul_path)
        os.makedirs(vul_path+'/img')

    # 下载图片
    for each in _vul_soup:
        # print each.get('src')
        # 获取详情页面的图片地址，后缀有可能为 png
        img_url = re.search(r'^(http|https://)(.*?)com/img(.*?).(jpeg|png)', each.get('src'), re.M | re.I)
        if img_url:
            # print type(img_url.group())
            # with open(vul_path+'/img/'+img_url.group()[-15:], 'a+') as jpeg:
                # 下载图片会损坏
                # jpeg.write(urllib2.urlopen(img_url.group()).read())
            # 图片保存至 img 文件夹下，判断是否存在
            if os.path.exists(vul_path+'/img/'+img_url.group()[-15:]):
                print title + 'Already Exists'
                pass
            else:
                urllib.urlretrieve(img_url.group(), vul_path+'/img/'+img_url.group()[-15:], call_back)

            img_list.append(str(img_url.group()))

    # 下载详情页面方法一，利用 urlretrieve
    # urllib.urlretrieve(url, '1.html', call_back)

    # 下载详情页面方法二，直接写，w+ 可读写，文件重写
    # 漏洞重名，这里采取了 url 链接后五位来避免重名
    with open(vul_path+'/'+title+url[-5:]+'.html', 'w+') as f:
        # 控制写入的内容，利用 for 循环一次性修改完成在进行写入
        html = str(vul_soup).replace('avatar" src=', 'avatar" src1=')

        for x in range(len(img_list)):
            html = html.replace('src="'+img_list[x], 'src="./img/'+img_list[x][-15:])

        f.write(html)


# 下载进度，a 已下载数据块，b 数据块大小，c 远程文件大小
def call_back(a, b, c):
    per = 100 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per


# 获取漏洞详情多线程
class VulThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            if vul_queue.empty(): break
            vul_url = vul_queue.get()
            vul_detail(vul_url)
            vul_queue.task_done()


def main(page_num, speed_num, thread_num):
    # global vul
    # vul = [] # 用队列替代了全局列表
    # vul 详情网址队列
    # 线程列表
    threads = []
    page_threads = []
    # 保存 vul 列表文件，单线程
    # for x in xrange(1, num+1):
    #     _url = 'http://sec.ly.com/bugs?page=' + str(x)
    #     url_soup(_url)
    # 多线程，保存 vul 列表文件
    for x in xrange(1, page_num+1):
        page_queue.put('http://sec.ly.com/bugs?page=' + str(x))

    for i in xrange(speed_num):
        page_threads.append(VulListThread())
        page_threads[i].start()

    for n in page_threads:
        n.join()

    save_result('Total:' + str(vul_queue.qsize()))
    print '=============================================='
    # 保存 vul 详情文件，单线程
    # for y in xrange(0, len(vul)):
    #     vul_detail('http://sec.ly.com/'+str(vul[y]))
    # 多线程
    for y in xrange(thread_num):
        threads.append(VulThread())
        threads[y].start()
    # 线程阻塞
    for z in threads:
        z.join()

if __name__ == '__main__':
    vul_queue = Queue()
    page_queue = Queue()
    start = time.time()
    args = parse_args()
    page_num = args.n
    speed_num = args.s
    thread_num = args.t
    main(page_num, speed_num, thread_num)
    print '====================Done====================='
    print time.time() - start
