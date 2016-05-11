#/user/bin/env python
# coding=utf-8

"""
Function: BuTian Company Spider
Author:   Pyx
Time:     2016年5月10日 15:16:16
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import argparse

# 简约模式
# for each in range(0, 2):
#     each = str(each)
#     url = "https://butian.360.cn/company/lists/page/%s" % each
#     resp = requests.get(url, verify=False)
#     # print resp.content
#     soup = BeautifulSoup(resp.content, 'html.parser', from_encoding='UTF-8')
#     tmp = soup.find_all('td')
#     for x in tmp:
#         # 判断厂商域名
#         if '.' in x.string:
#             print x.string
#             num.append(x.string)
#
# print len(num)
#


# 分析url
def url_resp(url):
    # 设置一个随机的用户代理，模拟浏览器
    user_agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                  "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]

    header = {'User-Agent': random.choice(user_agent)}
    # https 证书验证
    resp = requests.get(url, verify=False, headers=header)
    return resp


# 提取url页面中的company
def url_soup(url):
    soup = BeautifulSoup(url_resp(url).content, 'html.parser', from_encoding='UTF-8')
    _soup = soup.find_all('td')

    for each in _soup:
        if each.string == None:
            pass
        else:
            if '.' in each.string:
                print each.string
                save_result(each.string.encode('utf-8'))
        # print each.string

# 保存结果到txt文件
def save_result(company):
    report_name = 'BuTianCompany' + time.strftime('%Y%m%d', time.localtime()) + '.txt'
    with open(report_name, 'a+') as f:
        f.write(company)
        f.write('\n')


def main(p_num):
    for x in xrange(1, p_num+1):
        r_url = "https://butian.360.cn/company/lists/page/%s" % str(x)
        url_soup(r_url)
        print x


if __name__ == '__main__':
    # 默认106页
    parser = argparse.ArgumentParser(prog='BCSpider', usage='BCSpider.py [option]',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="* BuTian Company Spider *")
    parser.add_argument('-p', metavar='Page', default=106, type=int, help='The end page for crawling')
    arg = parser.parse_args()
    page = arg.p
    main(page)
    print "-----------------It's done-------------------"
