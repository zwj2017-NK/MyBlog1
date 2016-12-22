#!/usr/bin/env python
# coding=utf-8

import argparse
import sys

def parse_args():

    # 创建一个命令行参数对象
    parser = argparse.ArgumentParser(prog='BatchSqli', usage="BatchSqli.py [options]",
                                    description="* Batch Sql injection Scan *",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-t', metavar='ThreadNum', type=int, default=10, help='Num of threads')
    parser.add_argument('-u', metavar='UrlPath', type=str, default=r'./url.txt',
                        help="The url list for scanning")

    # 如果什么都没输入，就输入了一个脚本名，那么就是sys.argv只有一个参数
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    # 返回一个保存命令行参数的命名空间
    args = parser.parse_args()
    return args