#!/usr/bin/env python
# coding=utf-8

import argparse
import sys

def parse_args():

    # 创建一个命令行参数对象
    parser = argparse.ArgumentParser(prog='BuTianVulSpider', usage="ButianVul.py [options]",
                                    description="* BuTian Vulnerabilities Spider *",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s', metavar='StartPage', type=int, default=1, help='Start page for crawling')
    parser.add_argument('-e', metavar='EndPage', type=int, default=2, help='End page for crawling')
    parser.add_argument('-ct', metavar='CompanyThread', type=int, default=10, help='Num of company threads')
    parser.add_argument('-vt', metavar='VulThread', type=int, default=10, help='Num of vul threads')
    parser.add_argument('--company', default=False, action='store_true', help="Company Spider")
    parser.add_argument('--vul', default=False, action='store_true', help="Vulnerability Spider")
    parser.add_argument('--evul', default=False, action='store_true', help="Vul Exists")



    # 如果什么都没输入，就输入了一个脚本名，那么就是sys.argv只有一个参数
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    # 返回一个保存命令行参数的命名空间
    args = parser.parse_args()
    return args
