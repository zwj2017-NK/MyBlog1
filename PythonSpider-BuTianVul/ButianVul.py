#!/usr/bin/env python
# coding=utf-8

import requests
import random, re, time
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue
from pymongo import MongoClient
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

# 分析，获取数据
def url_soup(url):
    _url = 'http://new.butian.360.cn/Company/u/'
    soup = BeautifulSoup(url_resp(url).content, 'html.parser', from_encoding='UTF-8')
    # print soup
    # _soup = soup.find_all('dd')
    # print _soup
    # for each in _soup:
        # print each.contents
        # 获取每一页所有的漏洞名，隐藏版
        # for x in each.contents:
            # print type(x)
            # print x.string
        # 获取每一页显示厂商的漏洞，没有则 pass
        # if each.a:
            # 厂商链接 /Company/u/ + 厂商名
            # print each.a.get('href')
        # else:
            # pass
    # 直接用 href 属性正则匹配出每一页显示的厂商链接
    _soup = soup.find_all(href=re.compile(r'Company'))
    # print _soup
    for each in _soup:
        # print each.string
        company_url = _url + each.string
        print company_url
        company.append(company_url)
        # 简单的去重，数据库判断
        result = company_collection.find_one({'name': each.string})
        if result:
            pass
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            company_collection.insert_one({'name': each.string, 'url': company_url, 'time': now})
            print 'It has been successfully imported into the database.'



class CompanyUrl(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            if page_queue.empty(): break
            url = page_queue.get()
            url_soup(url)
            page_queue.task_done()


# 根据厂商，获取漏洞详细标题
def vul_soup(url):
    soup = BeautifulSoup(url_resp(url).content, 'html.parser', from_encoding='UTF-8')
    _soup = soup.find_all('var')
    vul = []
    if _soup:

        for each in _soup:
            # print each.contents[0]
            # print each.contents
            # 一些厂商的 St2 045 标题未显示，each.contents 长度为2，会出错，长度为3的不会出错
            if len(each.contents) == 3:
                vul.append(each.contents[0])
            # print vul
            # $inc 追加键值，只能用于追加整数、长整数、双精度浮点数
            # company_collection.update({'url': url}, {'$inc': {'vul': each.contents[0]}})
        # 简单的去重，数据库判断
        # result = company_collection.find_one({'vul': vul})
        # if result:
        #     pass
        # else:
        # $set 追加键值，如果有新漏洞，直接覆盖
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        company_collection.update({'url': url}, {'$set': {'vul': vul, 'time': now}})
        print vul
        print 'It has been successfully imported into the database.'
    else:
        company_collection.update({'url': url}, {'$set': {'vul': '公有SRC'}})
        print 'SRC has been successfully imported into the database.'





class CompanyVul(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while 1:
            if company_query.empty(): break
            url = company_query.get()
            vul_soup(url)
            company_query.task_done()



def main(g_company, s_page, e_page, cn_thread, g_vul, e_vul, vn_thread):

    threads = []
    vul_threads = []
    # 获取漏洞厂商
    if g_company:
        # 最后一页 6082，后面的无法获取
        for x in xrange(s_page, e_page+1):
            page_queue.put('http://new.butian.360.cn/Loo/index/p/' + str(x) + '.html')

        for y in xrange(cn_thread):
            threads.append(CompanyUrl())
            threads[y].start()

        for z in threads:
            z.join()

    # 获取漏洞标题
    if g_vul:
        # e_vul 判断是否没有 vul 字段
        if e_vul:
            today = time.strftime("%Y-%m-%d", time.localtime())

            for m in company_collection.find({'time': {'$gte': today}}):
                company_query.put(m['url'])
        else:
            i = 0
            for m in company_collection.find({'vul':{'$exists': False}}):
                company_query.put(m['url'])
                i = i + 1
                print 'Adding ' + str(i)
            print 'ALL datas have vul field.'

        for n in xrange(vn_thread):
            vul_threads.append(CompanyVul())
            vul_threads[n].start()

        for i in vul_threads:
            i.join()


if __name__ == '__main__':

    client = MongoClient('localhost', 27017)
    db = client.company
    company_collection = db.company_url
    # 获取的厂商名
    company = []
    # 漏洞页队列，用于获取厂商名
    page_queue = Queue()
    # 厂商队列，用于获取具体漏洞
    company_query = Queue()

    args = parse_args()
    page_s = args.s
    page_e = args.e
    company_t = args.ct
    vul_t = args.vt
    company_g = args.company
    vul_g = args.vul
    vul_e = args.evul
    start_time = time.time()
    print '===============Begin==============='
    main(company_g, page_s, page_e, company_t, vul_g, vul_e, vul_t)
    print '===============End================='
    print (time.time() - start_time) / 60